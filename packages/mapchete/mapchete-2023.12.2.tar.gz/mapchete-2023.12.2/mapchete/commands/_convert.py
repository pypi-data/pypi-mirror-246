import json
import logging
import os
from contextlib import AbstractContextManager
from multiprocessing import cpu_count
from pprint import pformat
from typing import List, Optional, Tuple, Type, Union

import tilematrix
from rasterio.crs import CRS
from rasterio.vrt import WarpedVRT
from shapely.geometry import box
from shapely.geometry.base import BaseGeometry

from mapchete.commands._execute import execute
from mapchete.commands.observer import ObserverProtocol, Observers
from mapchete.config import DaskSettings
from mapchete.config.parse import raw_conf, raw_conf_output_pyramid
from mapchete.errors import JobCancelledError
from mapchete.executor import Executor
from mapchete.formats import (
    available_input_formats,
    available_output_formats,
    driver_from_file,
)
from mapchete.io import MPath, fiona_open, get_best_zoom_level, rasterio_open, read_json
from mapchete.io.vector import reproject_geometry
from mapchete.tile import BufferedTilePyramid
from mapchete.types import MPathLike
from mapchete.validate import validate_zooms

logger = logging.getLogger(__name__)
OUTPUT_FORMATS = available_output_formats()


def convert(
    tiledir: MPathLike,
    output: MPathLike,
    zoom: Union[int, List[int]] = None,
    area: Union[BaseGeometry, str, dict] = None,
    area_crs: Union[CRS, str] = None,
    bounds: Tuple[float] = None,
    bounds_crs: Union[CRS, str] = None,
    point: Tuple[float, float] = None,
    point_crs: Tuple[float, float] = None,
    tile: Tuple[int, int, int] = None,
    overwrite: bool = False,
    concurrency: str = "processes",
    dask_settings: DaskSettings = DaskSettings(),
    workers: int = None,
    clip_geometry: str = None,
    bidx: List[int] = None,
    output_pyramid: str = None,
    output_metatiling: int = None,
    output_format: str = None,
    output_dtype: str = None,
    output_geometry_type: str = None,
    creation_options: dict = None,
    scale_ratio: float = None,
    scale_offset: float = None,
    resampling_method: str = "nearest",
    overviews: bool = False,
    overviews_resampling_method: str = "cubic_spline",
    cog: bool = False,
    src_fs_opts: Union[dict, None] = None,
    dst_fs_opts: Union[dict, None] = None,
    executor_getter: AbstractContextManager = Executor,
    observers: Optional[List[ObserverProtocol]] = None,
    retry_on_exception: Tuple[Type[Exception], Type[Exception]] = Exception,
    cancel_on_exception: Type[Exception] = JobCancelledError,
    retries: int = 0,
) -> None:
    """
    Convert mapchete outputs or other geodata.

    This is a wrapper around the mapchete.processes.convert process which helps generating tiled
    outputs for raster and vector data or single COGs from TileDirectory raster inputs.

    It also supports clipping of the input by a vector dataset.

    If only a subset of a TileDirectory is desired, please see the mapchete.commands.cp command.

    Parameters
    ----------
    tiledir : str
        Path to TileDirectory or mapchete config.
    output : str
        Path to output.
    zoom : integer or list of integers
        Single zoom, minimum and maximum zoom or a list of zoom levels.
    area : str, dict, BaseGeometry
        Geometry to override bounds or area provided in process configuration. Can be either a
        WKT string, a GeoJSON mapping, a shapely geometry or a path to a Fiona-readable file.
    area_crs : CRS or str
        CRS of area (default: process CRS).
    bounds : tuple
        Override bounds or area provided in process configuration.
    bounds_crs : CRS or str
        CRS of area (default: process CRS).
    point : iterable
        X and y coordinates of point whose corresponding process tile bounds will be used.
    point_crs : str or CRS
        CRS of point (defaults to process pyramid CRS).
    tile : tuple
        Zoom, row and column of tile to be processed (cannot be used with zoom)
    overwrite : bool
        Overwrite existing output.
    workers : int
        Number of execution workers when processing concurrently.
    concurrency : str
        Concurrency to be used. Could either be "processes", "threads" or "dask".
    dask_scheduler : str
        URL to dask scheduler if required.
    dask_max_submitted_tasks : int
        Make sure that not more tasks are submitted to dask scheduler at once. (default: 500)
    dask_chunksize : int
        Number of tasks submitted to the scheduler at once. (default: 100)
    dask_client : dask.distributed.Client
        Reusable Client instance if required. Otherwise a new client will be created.
    clip_geometry : str
        Path to Fiona-readable file by which output will be clipped.
    bidx : list of integers
        Band indexes to read from source.
    output_pyramid : str
        Output pyramid to write to. Can either be one of the standard pyramid grids or a JSON
        file holding the grid definition.
    output_metatiling : int
        Output metatiling.
    output_format : str
        Output format. Can be any raster or vector format available by mapchete.
    output_dtype : str
        Output data type (for raster output only).
    output_geometry_type :
        Output geometry type (for vector output only).
    creation_options : dict
        Output driver specific creation options.
    scale_ratio : float
        Scaling factor (for raster output only).
    scale_offset : float
        Scaling offset (for raster output only).
    resampling_method : str
        Resampling method used. (default: nearest).
    overviews : bool
        Generate overviews (single GTiff output only).
    overviews_resampling_method : str
        Resampling method used for overviews. (default: cubic_spline)
    cog : bool
        Write a valid COG. This will automatically generate verviews. (GTiff only)
    """

    all_observers = Observers(observers)
    workers = workers or cpu_count()
    creation_options = creation_options or {}
    bidx = [bidx] if isinstance(bidx, int) else bidx
    tiledir = MPath.from_inp(tiledir, storage_options=src_fs_opts)
    output = MPath.from_inp(output, storage_options=dst_fs_opts)
    try:
        input_info = _get_input_info(tiledir)
        logger.debug("input params: %s", input_info)
        output_info = _get_output_info(output)
        logger.debug("output params: %s", output_info)
    except Exception as e:
        raise ValueError(e)

    if (
        isinstance(output_pyramid, (str, MPath))
        and output_pyramid not in tilematrix._conf.PYRAMID_PARAMS.keys()
    ):
        output_pyramid = json.loads(MPath.from_inp(output_pyramid).read_text())

    # collect mapchete configuration
    mapchete_config = dict(
        process="mapchete.processes.convert",
        input=dict(inp=tiledir, clip=clip_geometry),
        pyramid=(
            dict(
                grid=output_pyramid,
                metatiling=(
                    output_metatiling
                    or (
                        input_info["pyramid"].get("metatiling", 1)
                        if input_info["pyramid"]
                        else 1
                    )
                ),
                pixelbuffer=(
                    input_info["pyramid"].get("pixelbuffer", 0)
                    if input_info["pyramid"]
                    else 0
                ),
            )
            if output_pyramid
            else input_info["pyramid"]
        ),
        output=dict(
            {
                k: v
                for k, v in input_info["output_params"].items()
                if k not in ["delimiters", "bounds", "mode"]
            },
            path=output,
            format=(
                output_format
                or output_info["driver"]
                or input_info["output_params"]["format"]
            ),
            dtype=output_dtype or input_info["output_params"].get("dtype"),
            **creation_options,
            **dict(overviews=True, overviews_resampling=overviews_resampling_method)
            if overviews
            else dict(),
        ),
        config_dir=os.getcwd(),
        zoom_levels=zoom or input_info["zoom_levels"],
        process_parameters=dict(
            scale_ratio=scale_ratio,
            scale_offset=scale_offset,
            resampling=resampling_method,
            band_indexes=bidx,
        ),
    )

    # assert all required information is there
    if mapchete_config["output"]["format"] is None:
        # this happens if input file is e.g. JPEG2000 and output is a tile directory
        raise ValueError("Output format required.")
    if mapchete_config["output"]["format"] == "GTiff":
        mapchete_config["output"].update(cog=cog)
    output_type = OUTPUT_FORMATS[mapchete_config["output"]["format"]]["data_type"]
    if bidx is not None:
        mapchete_config["output"].update(bands=len(bidx))
    if mapchete_config["pyramid"] is None:
        raise ValueError("Output pyramid required.")
    elif mapchete_config["zoom_levels"] is None:
        try:
            mapchete_config.update(
                zoom_levels=dict(
                    min=0,
                    max=get_best_zoom_level(
                        tiledir, mapchete_config["pyramid"]["grid"]
                    ),
                )
            )
        except Exception as exc:
            raise ValueError("Zoom levels required.") from exc
    elif input_info["input_type"] != output_type:
        raise ValueError(
            f"Output format type ({output_type}) is incompatible with input format ({input_info['input_type']})."
        )
    if output_metatiling:
        mapchete_config["pyramid"].update(metatiling=output_metatiling)
        mapchete_config["output"].update(metatiling=output_metatiling)
    if input_info["output_params"].get("schema") and output_geometry_type:
        mapchete_config["output"]["schema"].update(geometry=output_geometry_type)

    # determine process bounds
    out_pyramid = BufferedTilePyramid.from_dict(mapchete_config["pyramid"])
    inp_bounds = (
        bounds
        or reproject_geometry(
            box(*input_info["bounds"]),
            src_crs=input_info["crs"],
            dst_crs=out_pyramid.crs,
        ).bounds
        if input_info["bounds"]
        else out_pyramid.bounds
    )
    # if clip-geometry is available, intersect determined bounds with clip bounds
    if clip_geometry:
        clip_intersection = _clip_bbox(
            clip_geometry, dst_crs=out_pyramid.crs
        ).intersection(box(*inp_bounds))
        if clip_intersection.is_empty:
            all_observers.notify(
                message="Process area is empty: clip bounds don't intersect with input bounds."
            )
            return
    # add process bounds and output type
    mapchete_config.update(
        bounds=(clip_intersection.bounds if clip_geometry else inp_bounds),
        bounds_crs=bounds_crs,
    )
    mapchete_config["process_parameters"].update(
        clip_to_output_dtype=mapchete_config["output"].get("dtype", None),
    )
    logger.debug(f"temporary config generated: {pformat(mapchete_config)}")

    return execute(
        mapchete_config=mapchete_config,
        mode="overwrite" if overwrite else "continue",
        zoom=zoom,
        point=point,
        point_crs=point_crs,
        bounds=bounds,
        bounds_crs=bounds_crs,
        area=area,
        area_crs=area_crs,
        concurrency=concurrency,
        dask_settings=dask_settings,
        workers=workers,
        executor_getter=executor_getter,
        observers=observers,
        retry_on_exception=retry_on_exception,
        cancel_on_exception=cancel_on_exception,
        retries=retries,
    )


def _clip_bbox(clip_geometry, dst_crs=None):
    with fiona_open(clip_geometry) as src:
        return reproject_geometry(box(*src.bounds), src_crs=src.crs, dst_crs=dst_crs)


def _get_input_info(inp):
    # assuming single file if path has a file extension
    if inp.suffix:
        logger.debug("assuming single file")
        driver = driver_from_file(inp)

        # single file input can be a mapchete file or a rasterio/fiona file
        if driver == "Mapchete":
            logger.debug("input is mapchete file")
            input_info = _input_mapchete_info(inp)

        elif driver == "raster_file":
            # this should be readable by rasterio
            logger.debug("input is raster_file")
            input_info = _input_rasterio_info(inp)

        elif driver == "vector_file":
            # this should be readable by Fiona
            input_info = _input_fiona_info(inp)
        else:  # pragma: no cover
            raise NotImplementedError(f"driver {driver} is not supported")

    # assuming tile directory
    else:
        logger.debug("input is tile directory")
        input_info = _input_tile_directory_info(inp)

    return input_info


def _input_mapchete_info(inp):
    conf = raw_conf(inp)
    output_params = conf["output"]
    pyramid = raw_conf_output_pyramid(conf)
    return dict(
        output_params=output_params,
        pyramid=pyramid.to_dict(),
        crs=pyramid.crs,
        zoom_levels=validate_zooms(conf["zoom_levels"], expand=False),
        pixel_size=None,
        input_type=OUTPUT_FORMATS[output_params["format"]]["data_type"],
        bounds=conf.get("bounds"),
    )


def _input_rasterio_info(inp):
    with rasterio_open(inp) as src:
        if src.transform.is_identity:
            if src.gcps[1] is not None:
                with WarpedVRT(src) as dst:
                    bounds = dst.bounds
                    crs = src.gcps[1]
            elif src.rpcs:  # pragma: no cover
                with WarpedVRT(src) as dst:
                    bounds = dst.bounds
                    crs = CRS.from_string("EPSG:4326")
            else:  # pragma: no cover
                raise TypeError("cannot determine georeference")
        else:
            crs = src.crs
            bounds = src.bounds
        return dict(
            output_params=dict(
                bands=src.meta["count"],
                dtype=src.meta["dtype"],
                format=src.driver if src.driver in available_input_formats() else None,
            ),
            pyramid=None,
            crs=crs,
            zoom_levels=None,
            pixel_size=src.transform[0],
            input_type="raster",
            bounds=bounds,
        )


def _input_fiona_info(inp):
    with fiona_open(inp) as src:
        return dict(
            output_params=dict(
                schema=src.schema,
                format=src.driver if src.driver in available_input_formats() else None,
            ),
            pyramid=None,
            crs=src.crs,
            zoom_levels=None,
            input_type="vector",
            bounds=src.bounds if len(src) else None,
        )


def _input_tile_directory_info(tiledir_path):
    conf = read_json(tiledir_path / "metadata.json")
    pyramid = BufferedTilePyramid.from_dict(conf["pyramid"])
    return dict(
        output_params=conf["driver"],
        pyramid=pyramid.to_dict(),
        crs=pyramid.crs,
        zoom_levels=None,
        pixel_size=None,
        input_type=OUTPUT_FORMATS[conf["driver"]["format"]]["data_type"],
        bounds=None,
    )


def _get_output_info(output):
    if not output.suffix:
        return dict(type="TileDirectory", driver=None)
    elif output.suffix == ".tif":
        return dict(type="SingleFile", driver="GTiff")
    else:
        raise TypeError(f"Could not determine output from extension: {output.suffix}")

import logging
import pathlib
import re
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.responses import RedirectResponse
from planetreference.config import tortoise_config
from starlette.status import HTTP_400_BAD_REQUEST
from tortoise import Tortoise
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.functions import Lower

from ..business import WktDatabase
from ..models import WKT_model, Wkt_Pydantic
from ..models import CenterCs

logger = logging.getLogger(__name__)

router = APIRouter()
# https://datacarpentry.org/python-ecology-lesson/09-working-with-sql/index.html


@router.get(
    "/wkts", response_model=List[Wkt_Pydantic], description="List all WKTs"
)
async def get_wkts(
    limit: Optional[int] = Query(
        50, description="Number of records to display", gt=0, le=100
    ),
    offset: Optional[int] = Query(
        0, description="Number of record from which we start to display", gt=-1
    ),
):
    return await Wkt_Pydantic.from_queryset(
        WKT_model.all()
        .limit(limit if limit else limit.default)
        .offset(offset if offset else offset.default)
    )


@router.get(
    "/wkts/versions",
    response_model=List[int],
    description="List all available versions of the WKT.",
)
async def get_versions():
    objs = (
        await WKT_model.all()
        .group_by("version")
        .order_by("version")
        .values("version")
    )
    versions = list()
    for obj in objs:
        versions.append(obj["version"])
    return versions


@router.get(
    "/wkts/versions/{version_id}",
    response_model=List[Wkt_Pydantic],
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPNotFoundError}},
    description="List WKTs for a given version",
)
async def get_version(
    version_id: int = Path(
        default=2015, description="Version of the WKT", gt=0
    ),
    limit: Optional[int] = Query(
        50, description="Number of records to display", gt=0, le=100
    ),
    offset: Optional[int] = Query(
        0, description="Number of record from which we start to display", gt=0
    ),
):
    obj = (
        await WKT_model.filter(version=version_id)
        .limit(limit if limit else limit.default)
        .offset(offset if offset else offset.default)
    )
    if len(obj) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{version_id} not found",
        )
    return obj


@router.get(
    "/wkts/versions/{version_id}/{wkt_id}",
    response_model=str,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPNotFoundError},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPNotFoundError},
    },
)
async def get_wkt_version(
    version_id: int = Path(
        default=2015, description="Version of the WKT", gt=0
    ),
    wkt_id: str = Path(
        default="IAU:2015:1000",
        description="Identifier of the WKT",
        regex="^.*:\d*:\d*$",
    ),
):
    m = re.match(r"IAU:(?P<version>.*):(?P<wkt>.*)", wkt_id)
    if m is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{wkt_id} pattern is not recognized",
        )
    elif m.group("version") != str(version_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{wkt_id} is not part of the WKTs in {version_id}",
        )
    else:
        return RedirectResponse(url=f"/ws/wkts/{wkt_id}")


@router.get(
    "/wkts/{wkt_id}",
    response_model=str,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPNotFoundError}},
    description="Retrieve a WKT for a given WKT ID.",
)
async def get_wkt(
    wkt_id: str = Path(
        default="IAU:2015:1000",
        title="ID of the WKT.",
        description="ID of the WKT following this pattern : IAU:<version>:<code>",
        regex="^.*:\d*:\d*",
    ),
):
    obj = await WKT_model.get_or_none(id=wkt_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{wkt_id} not found"
        )
    wkt_obj: WKT_model = await Wkt_Pydantic.from_tortoise_orm(obj)
    return wkt_obj.wkt


@router.get("/solar_bodies", response_model=List[str])
async def get_solar_bodies():
    objs = (
        await WKT_model.all()
        .group_by("solar_body")
        .order_by("solar_body")
        .values("solar_body")
    )
    solar_bodies = list()
    for obj in objs:
        solar_bodies.append(obj["solar_body"])
    return solar_bodies


@router.get(
    "/solar_bodies/{solar_body}",
    response_model=List[Wkt_Pydantic],
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPNotFoundError}},
)
async def get_solar_body(solar_body: str):
    obj = await WKT_model.annotate(
        solar_body_lower=Lower("solar_body")
    ).filter(solar_body_lower=solar_body.lower())
    if len(obj) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{solar_body} not found",
        )
    return obj


@router.on_event("startup")
async def startup_event():
    pattern = "sqlite://(?P<db_name>.*)"
    m = re.match(pattern, tortoise_config.db_url)
    file = None
    if m is not None:
        file = pathlib.Path(m.group("db_name"))

    if file is None or not file.exists():
        await Tortoise.init(
            db_url=tortoise_config.db_url, modules=tortoise_config.modules
        )
        await Tortoise.generate_schemas()
        wkt = WktDatabase()
        index = wkt.index
        logger.info(f"nb records : {len(index)}")
        for record in index:
            wkt_data = {
                "id": f"IAU:{record.iau_version}:{record.iau_code}",
                "version": int(record.iau_version),
                "code": int(record.iau_code),
                "center_cs": CenterCs.find_enum(record.origin_crs),
                "solar_body": re.match(r"[^\s]+", record.datum).group(0),
                "datum_name": record.datum,
                "ellipsoid_name": record.ellipsoid,
                "projection_name": record.projcrs,
                "wkt": record.wkt,
            }
            await WKT_model.create(**wkt_data)
    else:
        logger.info("loading the db")


@router.on_event("shutdown")
async def close_orm():
    await Tortoise.close_connections()

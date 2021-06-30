from fastapi import FastAPI
from tortoise.contrib.starlette import register_tortoise

from .config import tortoise_config

def init(app: FastAPI):
    """
    Init routers and etc.
    :return:
    """
    init_routers(app)
    init_db(app)


def init_db(app: FastAPI):
    """
    Init database models.
    :param app:
    :return:
    """
    register_tortoise(
        app,
        db_url=tortoise_config.db_url,
        generate_schemas=tortoise_config.generate_schemas,
        modules=tortoise_config.modules,
    )


def init_routers(app: FastAPI):
    """
    Initialize routers defined in `app.api`
    :param app:
    :return:
    """
    from .core.routers import router_web_site, router_ws

    app.include_router(
        router_ws,
        tags=["API"],
        prefix="/ws",
        responses={404: {"description": "Not found"}},
    )
    app.include_router(
        router_web_site,
        tags=["Web site"],
        responses={404: {"description": "Not found"}},
    )

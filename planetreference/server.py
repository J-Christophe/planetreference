from fastapi import FastAPI
import logging

from .config import openapi_config
from .initializer import init

logger = logging.getLogger(__name__)

app = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
)
logger.info("Starting application initialization...")
init(app)
logger.info("Successfully initialized!")

"""
Models - database and pydantic models of API entities.
"""
from .tortoise import WKT as WKT_model
from .pydantic import Wkt_Pydantic

__all__ = [
    "WKT_model",
    "Wkt_Pydantic"
]

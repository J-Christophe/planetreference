from tortoise import fields, models
from enum import Enum


class CenterCs(str, Enum):
    OCENTRIC = "OCENTRIC"
    OGRAPHIC = "OGRAPHIC"


class WKT(models.Model):
    """
    This references a WKT
    """

    id = fields.CharField(
        pk=True,
        max_length=100,
        description="ID of WKT. Pattern of the ID is the following IAU:<version>:<code>",
    )
    version = fields.IntField(index=True, description="Version of the WKT")
    code = fields.IntField(indexed=True, description="WKT code")
    solar_body = fields.CharField(
        max_length=100,
        indexed=True,
        description="Solar body such as Mercury, Venus, ...",
    )
    center_cs = fields.CharEnumField(
        CenterCs,
        default=CenterCs.OGRAPHIC,
        indexed=True,
        description="Center of the coordinate system",
    )
    datum_name = fields.CharField(
        max_length=100, indexed=True, description="Datum name"
    )
    ellipsoid_name = fields.CharField(
        max_length=100, indexed=True, description="Ellispoid name"
    )
    projection_name = fields.CharField(
        max_length=100, indexed=True, null=True, description="Projection name"
    )
    wkt = fields.CharField(max_length=3072, description="WKT")

    #: The date-time the Tournament record was created at
    created_at = fields.DatetimeField(auto_now_add=True)

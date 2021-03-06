"""Config of DB"""
from pydantic import Field

from .base import BaseSettings
from .cfg import IS_TEST

DB_MODELS = ["planetreference.core.models.tortoise"]
POSTGRES_DB_URL = "postgres://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
SQLITE_DB_URL = "sqlite://{sqlite_db}"  # sqlite://:memory:"


class SqlLiteSettings(BaseSettings):
    """SQL liste env values"""

    sqlite_db: str = Field("db.sqlite3", env="SQLITE_DB")


class PostgresSettings(BaseSettings):
    """Postgres env values"""

    postgres_user: str = Field("postgres", env="POSTGRES_USER")
    postgres_password: str = Field("postgres", env="POSTGRES_PASSWORD")
    postgres_db: str = Field("mydb", env="POSTGRES_DB")
    postgres_port: str = Field("5432", env="POSTGRES_PORT")
    postgres_host: str = Field("postgres", env="POSTGRES_HOST")


class TortoiseSettings(BaseSettings):
    """Tortoise-ORM settings"""

    db_url: str
    modules: dict
    generate_schemas: bool

    @classmethod
    def generate(cls):
        """Generate Tortoise-ORM settings (with sqlite if tests)"""

        if IS_TEST:
            sqlite = SqlLiteSettings()
            db_url = SQLITE_DB_URL.format(**sqlite.dict())
            del sqlite
        else:
            postgres = PostgresSettings()
            db_url = POSTGRES_DB_URL.format(**postgres.dict())
            del postgres
        modules = {"models": DB_MODELS}
        return TortoiseSettings(
            db_url=db_url, modules=modules, generate_schemas=True
        )

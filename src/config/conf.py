import os
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator

BATCH = int(os.getenv("BATCH", "10"))


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = {"pool_pre_ping": True}

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"postgresql+asyncpg://{values.get('DB_USER')}:{values.get('DB_PASSWORD')}@{values.get('DB_HOST')}:{values.get('DB_PORT')}/{values.get('DB_NAME')}"


class Settings(DBSettings):
    """
    Basic Settings
    """

    ENV: str = "local"


def get_settings() -> Settings:
    configs = {
        "migration": DBSettings,
        "local": Settings,
    }
    _env = os.getenv("ENV", "local")
    return configs.get(_env)()


settings = get_settings()

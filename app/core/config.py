import os
from typing import List, Union
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SecureChain Portal API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://securechain-alb-dev-263833044.us-east-1.elb.amazonaws.com",
    ]

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "securechain_admin"
    POSTGRES_PASSWORD: str = "securechain_secret"
    POSTGRES_DB: str = "securechain_db"
    SQLALCHEMY_DATABASE_URI: Union[str, None] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Union[str, None], info) -> str:
        if isinstance(v, str) and v:
            return v
        values = info.data
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        server = values.get("POSTGRES_SERVER")
        port = values.get("POSTGRES_PORT")
        db = values.get("POSTGRES_DB")
        return f"postgresql://{user}:{password}@{server}:{port}/{db}"

    SECRET_KEY: str = "CHANGE_THIS_TO_A_SECURE_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
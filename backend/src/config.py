from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path("./.env"), env_file_encoding="utf-8")

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    access_token_expire: int
    refresh_token_expire: int
    jwt_secret: str
    jwt_algorithm: str

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@"
            f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
        )


settings = Settings()

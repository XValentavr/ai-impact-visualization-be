from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseModel):
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)
    CORS_ALLOW_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    # move outside the app directory to avoid infinite loop
    LOG_FILE_PATH: str = Field(default="./logs/application.log")
    DATA_DIR: str = Field(default="./app/data")

    @property
    def data_dir_path(self) -> Path:
        return Path(self.DATA_DIR)


class PostgresSettings(BaseModel):
    USER: str = Field(default="ai_impact_user")
    PASSWORD: str = Field(default="ai_impact_password")
    HOST: str = Field(default="localhost")
    PORT: int = Field(default=5432)
    DATABASE: str = Field(default="ai_impact_db")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


class Settings(BaseSettings):
    server: ServerSettings = ServerSettings()
    postgres: PostgresSettings = PostgresSettings()

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

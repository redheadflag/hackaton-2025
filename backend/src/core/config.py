from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class BackendSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding='utf-8',
        extra="ignore",

        env_prefix="BACKEND_"
    )

    port: int
    allowed_hosts: list[str]
    api_endpoint: str


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding='utf-8',
        env_prefix="POSTGRES_",

        extra="ignore"
    )

    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


backend_settings = BackendSettings()  # type: ignore
database_settings = DatabaseSettings()  # type: ignore

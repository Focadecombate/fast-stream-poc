from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    rabbit_url: str = "amqp://guest:guest@localhost:5672/"
    log_level: str = "INFO"
    database_url: str = "sqlite+aiosqlite:///./faststream_poc.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

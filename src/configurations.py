from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    slack_signing_secret: str
    slack_client_id: str
    slack_client_secret: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
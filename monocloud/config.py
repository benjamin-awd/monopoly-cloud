import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class CloudSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    project_id: str = ""
    secret_id: str = ""
    trusted_user_emails: list[str] = []
    gmail_address: str = ""
    pubsub_topic: str = ""
    gcs_bucket: str = ""


cloud_settings = CloudSettings()

import json
import logging
from functools import lru_cache
from typing import Any, Type

from pydantic import SecretStr
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

logger = logging.getLogger(__name__)


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    project_id: str = ""
    secret_id: str = ""
    trusted_user_emails: list = []
    gmail_address: str = ""
    pubsub_topic: str = ""
    gcs_bucket: str = ""


# pylint: disable=too-many-arguments
class CloudSettings(EnvSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    ocbc_pdf_passwords: list[SecretStr] = [""]
    citibank_pdf_passwords: list[SecretStr] = [""]
    standard_chartered_pdf_passwords: list[SecretStr] = [""]
    hsbc_pdf_passwords: list[SecretStr] = [""]

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            JsonFileSecretMount(settings_cls),
            dotenv_settings,
            env_settings,
            file_secret_settings,
        )


# pylint: disable=arguments-differ
class JsonFileSecretMount(PydanticBaseSettingsSource):
    @lru_cache
    def get_secrets(self, file_path="/run/secrets/monopoly.json") -> dict[str, Any]:
        try:
            with open(file_path, encoding="utf-8") as file:
                secrets: dict[str, Any] = json.load(file)
                return {k.lower(): v for k, v in secrets.items()}

        except FileNotFoundError as err:
            logger.warning(
                "Could not access secret mount: %s %s",
                "loading from .env instead.",
                err,
            )
            return {}

    def get_field_value(self, field_name: str) -> tuple[Any, str]:
        secrets = self.get_secrets()
        field_value = secrets.get(field_name)
        return field_value, field_name

    def __call__(self) -> dict[str, Any]:
        values_dict = {}
        for field_name in self.settings_cls.model_fields.keys():
            field_value, field_key = self.get_field_value(field_name)
            if field_value is not None:
                values_dict[field_key] = field_value
        return values_dict


cloud_settings = CloudSettings()

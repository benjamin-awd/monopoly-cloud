from pydantic_settings import BaseSettings, SettingsConfigDict


class CloudSettings(BaseSettings):
    gmail_address: str = ""
    project_id: str = ""
    pubsub_topic: str = ""
    secret_id: str = ""
    gcs_bucket: str = ""
    ocbc_pdf_passwords: str = ""
    citibank_pdf_passwords: str = ""
    standard_chartered_pdf_passwords: str = ""
    hsbc_pdf_passwords: str = ""
    trusted_user_emails: list = []

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


cloud_settings = CloudSettings()

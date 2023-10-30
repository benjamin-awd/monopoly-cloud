import logging
import os
from typing import Optional

from google.cloud import storage  # type: ignore
from monopoly.statement import Statement
from monopoly.storage import generate_name, write_to_csv
from pandas import DataFrame

from monocloud.config import cloud_settings

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)


def upload_to_cloud_storage(
    source_filename: str,
    bucket_name: str,
    statement: Statement,
) -> None:
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    blob_name = generate_name("blob", statement.config, statement.statement_date)
    blob = bucket.blob(blob_name)

    logger.info(f"Attempting to upload to 'gs://{bucket_name}/{blob_name}'")
    blob.upload_from_filename(source_filename)
    logger.info("Uploaded to %s", blob_name)


def load(
    df: DataFrame,
    statement: Statement,
    csv_file_path: Optional[str] = None,
):
    filename = generate_name("file", statement.config, statement.statement_date)
    csv_file_path = os.path.join(ROOT_DIR, "output", filename)
    logger.info("Writing CSV to file path: %s", csv_file_path)

    csv_file_path = write_to_csv(df, csv_file_path=csv_file_path, statement=statement)

    upload_to_cloud_storage(
        statement=statement,
        source_filename=csv_file_path,  # type: ignore
        bucket_name=cloud_settings.gcs_bucket,
    )

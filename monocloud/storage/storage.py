import logging
from pathlib import Path

from google.cloud import storage  # type: ignore
from monopoly.statements import CreditStatement, DebitStatement
from monopoly.write import generate_name

logger = logging.getLogger(__name__)


def upload_to_cloud_storage(
    file_path: Path,
    bucket_name: str,
    statement: CreditStatement | DebitStatement,
) -> None:
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob_name = generate_name(
        document=statement.document,
        format_type="blob",
        statement_config=statement.config,
        statement_type=statement.statement_type,
        statement_date=statement.statement_date,
    )
    blob = bucket.blob(blob_name)

    logger.debug(f"Attempting to upload to 'gs://{bucket_name}/{blob_name}'")
    blob.upload_from_filename(file_path)
    logger.info("Uploaded to %s", blob_name)

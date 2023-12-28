import logging
from pathlib import Path

from google.cloud import storage  # type: ignore
from monopoly.statements import CreditStatement, DebitStatement
from monopoly.write import generate_name
from pandas import DataFrame

logger = logging.getLogger(__name__)


def upload_to_cloud_storage(
    source_filename: str,
    bucket_name: str,
    statement: CreditStatement | DebitStatement,
) -> None:
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob_name = generate_name(
        file_path=source_filename,
        format_type="blob",
        statement_config=statement.statement_config,
        statement_type=statement.statement_type,
        statement_date=statement.statement_date,
    )
    blob = bucket.blob(blob_name)

    logger.info(f"Attempting to upload to 'gs://{bucket_name}/{blob_name}'")
    blob.upload_from_filename(source_filename)
    logger.info("Uploaded to %s", blob_name)


def load(
    df: DataFrame,
    statement: CreditStatement | DebitStatement,
    output_directory: Path,
    file_path: Path,
):
    if isinstance(output_directory, str):
        output_directory = Path(output_directory)

    filename = generate_name(
        file_path=file_path,
        format_type="file",
        statement_config=statement.statement_config,
        statement_type=statement.statement_type,
        statement_date=statement.statement_date,
    )
    output_path = output_directory / filename
    logger.debug("Writing CSV to file path: %s", output_path)
    df.to_csv(output_path, index=False)

    return output_path

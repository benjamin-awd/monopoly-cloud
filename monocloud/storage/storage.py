import logging
from datetime import datetime
from pathlib import Path

from fitz import Document
from google.cloud import storage  # type: ignore
from monopoly.config import StatementConfig
from monopoly.statements import CreditStatement, DebitStatement
from monopoly.write import generate_hash, generate_name
from pandas import DataFrame

logger = logging.getLogger(__name__)


def generate_blob_name(
    document: Document,
    statement_config: StatementConfig,
    statement_type: str,
    statement_date: datetime,
    file_suffix="csv",
) -> str:
    """
    Generates a blob name for Google Cloud Storage

    Partitions by bank name, account type, year month and statement UUID
    """
    bank_name = statement_config.bank_name
    year = statement_date.year
    month = statement_date.month
    file_uuid = generate_hash(document)

    filename = (
        f"{bank_name}-{statement_type}-{year}-{month:02d}-{file_uuid}.{file_suffix}"
    )

    blob_name = (
        f"bank_name={bank_name}/"
        f"account_type={statement_type}/"
        f"statement_date={statement_date.isoformat()[:10]}/"
        f"{filename}"
    )
    return blob_name


def upload_to_cloud_storage(
    file_path: Path,
    bucket_name: str,
    statement: CreditStatement | DebitStatement,
) -> None:
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob_name = generate_blob_name(
        document=statement.document,
        statement_config=statement.statement_config,
        statement_type=statement.statement_type,
        statement_date=statement.statement_date,
    )
    blob = bucket.blob(blob_name)

    logger.debug(f"Attempting to upload to 'gs://{bucket_name}/{blob_name}'")
    blob.upload_from_filename(file_path)
    logger.info("Uploaded to %s", blob_name)


def load(
    df: DataFrame, statement: CreditStatement | DebitStatement, output_directory: Path
):
    if isinstance(output_directory, str):
        output_directory = Path(output_directory)

    filename = generate_name(
        document=statement.document,
        format_type="file",
        statement_config=statement.statement_config,
        statement_type=statement.statement_type,
        statement_date=statement.statement_date,
    )
    output_path = output_directory / filename
    logger.debug("Writing CSV to file path: %s", output_path)
    df.to_csv(output_path, index=False)

    return output_path

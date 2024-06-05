# pylint: disable=broad-exception-caught
import logging
import sys
from pathlib import Path

from monopoly.pipeline import Pipeline

from monocloud.config import cloud_settings
from monocloud.gmail import Gmail, Message
from monocloud.gmail.exceptions import AttachmentNotFoundError
from monocloud.storage import upload_to_cloud_storage

logger = logging.getLogger(__name__)


def main():
    """
    Entrypoint for Cloud Run function that extracts bank statement,
    transforms it, then loads it to disk or cloud
    """
    logger.info("Beginning bank statement extraction")
    messages: list[Message] = Gmail().get_emails()
    unhandled_exceptions = False

    for message in messages:
        try:
            process_bank_statement(message, upload_to_cloud=True)
        except AttachmentNotFoundError as err:
            logger.error(err, exc_info=True)
            message.mark_as_spam()
        except Exception as err:
            unhandled_exceptions = True
            logger.error(err, exc_info=True)

    if unhandled_exceptions:
        sys.exit(1)


def run_pipeline(file_path, upload_to_cloud: bool, output_dir: Path = Path(".")):
    """
    Runs the pipeline on a file, and returns the path to the
    processed CSV
    """
    pipeline = Pipeline(file_path)
    statement = pipeline.extract()
    transactions = pipeline.transform(statement)
    processed_file_path = pipeline.load(
        transactions=transactions, statement=statement, output_directory=output_dir
    )
    logger.info("Created file: %s", processed_file_path)
    if upload_to_cloud:
        upload_to_cloud_storage(
            processed_file_path, cloud_settings.gcs_bucket, statement
        )
    return processed_file_path


def process_bank_statement(message: Message, upload_to_cloud: bool):
    """
    Process a bank statement using the provided bank class.

    If an error occurs, the statement is removed from disk
    """
    attachment = message.get_attachment()
    with message.save(attachment) as file_path:  # type: ignore
        try:
            file_path = run_pipeline(file_path, upload_to_cloud)
            message.mark_as_read()
        except Exception as err:
            logger.error(err, exc_info=True)
    return file_path


if __name__ == "__main__":
    main()

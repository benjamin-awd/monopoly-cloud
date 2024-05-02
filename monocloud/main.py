# pylint: disable=broad-exception-caught
import logging
import sys
from pathlib import Path

from monopoly.processors import detect_processor

from monocloud.config import cloud_settings
from monocloud.gmail import Gmail, Message
from monocloud.gmail.exceptions import AttachmentNotFoundError
from monocloud.storage import load, upload_to_cloud_storage

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
            process_bank_statement(message)
        except AttachmentNotFoundError as err:
            logger.error(err, exc_info=True)
            message.mark_as_spam()
        except Exception as err:
            unhandled_exceptions = True
            logger.error(err, exc_info=True)

    if unhandled_exceptions:
        sys.exit(1)


def process_bank_statement(message: Message, upload_to_cloud: bool = True):
    """
    Process a bank statement using the provided bank class.

    If an error occurs, the statement is removed from disk
    """
    attachment = message.get_attachment()
    with message.save(attachment) as file_path:  # type: ignore
        processor = detect_processor(file_path=file_path)
        statement = processor.extract()
        transformed_df = processor.transform(statement)

        if upload_to_cloud:
            processed_file_path = load(
                df=transformed_df, statement=statement, output_directory=Path(".")
            )

            try:
                upload_to_cloud_storage(
                    processed_file_path, cloud_settings.gcs_bucket, statement
                )
                message.mark_as_read()
            except Exception as err:
                logger.error(err, exc_info=True)


if __name__ == "__main__":
    main()

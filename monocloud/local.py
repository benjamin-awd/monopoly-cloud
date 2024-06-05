from concurrent.futures import ThreadPoolExecutor
from glob import glob
from pathlib import Path

from monopoly.pipeline import Pipeline

from monocloud.config import cloud_settings
from monocloud.storage import upload_to_cloud_storage


def process_and_upload(file_path, upload_to_cloud: bool = False):
    pipeline = Pipeline(file_path)
    statement = pipeline.extract()
    transactions = pipeline.transform(statement)
    processed_file_path = pipeline.load(
        transactions=transactions,
        statement=statement,
        output_directory=Path("./output"),
    )
    if upload_to_cloud:
        upload_to_cloud_storage(
            processed_file_path, cloud_settings.gcs_bucket, statement
        )


def upload_from_local():
    """Helper function to upload files to cloud storage from local"""
    statements = glob("statements/**/*.pdf", recursive=True)

    with ThreadPoolExecutor() as executor:
        executor.map(process_and_upload, statements)


if __name__ == "__main__":
    upload_from_local()

from concurrent.futures import ThreadPoolExecutor
from glob import glob

from monopoly.processors import detect_processor

from monocloud.config import cloud_settings
from monocloud.storage import upload_to_cloud_storage


def process_and_upload(file_path):
    processor = detect_processor(file_path=file_path)
    statement = processor.extract()
    transformed_df = processor.transform(statement)
    processed_file_path = processor.load(
        transformed_df, statement, output_directory="./output"
    )
    upload_to_cloud_storage(processed_file_path, cloud_settings.gcs_bucket, statement)


def upload_from_local():
    """Helper function to upload files to cloud storage from local"""
    statements = glob("statements/**/*.pdf", recursive=True)

    with ThreadPoolExecutor() as executor:
        executor.map(process_and_upload, statements)


if __name__ == "__main__":
    upload_from_local()

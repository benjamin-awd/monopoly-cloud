import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from glob import glob
from pathlib import Path

from monocloud.main import run_pipeline

logger = logging.getLogger(__name__)


def upload_from_local(upload_to_cloud: bool, single_process: bool, output_dir: Path):
    """Helper function to upload files to cloud storage from local"""
    statements = glob("statements/**/*.pdf", recursive=True)
    if single_process:
        for statement in statements:
            run_pipeline(
                statement, upload_to_cloud=upload_to_cloud, output_dir=output_dir
            )

    else:
        process_func = partial(
            run_pipeline, upload_to_cloud=upload_to_cloud, output_dir=output_dir
        )
        with ThreadPoolExecutor() as executor:
            executor.map(process_func, statements)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and upload bank statements.")
    parser.add_argument(
        "--local", action="store_true", help="Process statements from local files"
    )
    parser.add_argument(
        "--upload", action="store_true", help="Upload processed statements to the cloud"
    )
    parser.add_argument(
        "--single",
        action="store_true",
        help="Run in single-threaded mode",
        default=True,
    )
    parser.add_argument(
        "--output", help="Controls output directory", default="./output"
    )
    args = parser.parse_args()
    upload_from_local(
        upload_to_cloud=args.local or args.upload,
        single_process=args.single,
        output_dir=args.output,
    )

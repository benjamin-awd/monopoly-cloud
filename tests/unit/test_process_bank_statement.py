from pathlib import Path

from monocloud.main import process_bank_statement


def test_process_bank_statement(message_with_example_statement):
    output_path = process_bank_statement(
        message_with_example_statement, upload_to_cloud=False
    )
    assert output_path == Path("example-credit-2023-07-9a7ca0.csv")

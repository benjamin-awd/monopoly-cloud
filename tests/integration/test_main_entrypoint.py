"""Test for entrypoint used by Cloud Run"""

from unittest.mock import Mock, PropertyMock, patch

from monocloud.main import process_bank_statement


def run_bank_statement_test(message, pattern, subject, expected_result):
    with patch(
        "monocloud.main.Message.subject", new_callable=PropertyMock
    ) as mock_subject:
        mock_subject.return_value = subject
        bank_class = Mock()
        banks = {pattern: bank_class}

        process_bank_statement(message, banks, upload_to_cloud=False)

        if expected_result == "call":
            bank_class.assert_called_once()

        else:
            bank_class.assert_not_called()

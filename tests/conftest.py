from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

from monocloud.gmail import Message, MessageAttachment


@pytest.fixture
def message_with_example_statement():
    # Create a mock message object
    message = MagicMock(spec=Message)
    message.get_attachment.return_value = b"mock_attachment_content"

    # Mock the save method to act as a context manager
    message.save.return_value.__enter__.return_value = Path(
        "tests/example_statement.pdf"
    )
    message.save.return_value.__exit__ = MagicMock()
    yield message


@pytest.fixture(scope="session")
def message():
    yield Message(data={}, gmail_service=Mock())


@pytest.fixture(scope="session")
def attachment():
    yield MessageAttachment(filename="test.pdf", file_byte_string=b"Test data")

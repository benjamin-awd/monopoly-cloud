from unittest import mock

import pytest

from monocloud.gmail import Message, MessageAttachment


@pytest.fixture(scope="session")
def message():
    return Message(data={}, gmail_service=mock.Mock())


@pytest.fixture(scope="session")
def attachment():
    return MessageAttachment(filename="test.pdf", file_byte_string=b"Test data")

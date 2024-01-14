import pytest

from monocloud.gmail import Message
from monocloud.gmail.exceptions import AttachmentNotFoundError, MultipleAttachmentsError


def test_message_with_part_attachment(message: Message):
    data = {
        "payload": {
            "filename": "",
            "parts": [
                {
                    "partId": "1",
                    "filename": "file1.txt",
                    "body": {"attachmentId": "123"},
                }
            ],
        }
    }
    message.payload = data["payload"]
    attachment_id, filename = message.get_attachment_metadata()
    assert filename == "file1.txt"
    assert attachment_id == "123"


def test_message_with_multiple_attachment(message: Message):
    data = {
        "payload": {
            "parts": [
                {
                    "partId": "1",
                    "filename": "file1.txt",
                    "body": {"attachmentId": "123"},
                },
                {
                    "partId": "2",
                    "body": {"attachmentId": "456"},
                    "parts": [
                        {
                            "partId": "3",
                            "filename": "file2.txt",
                            "body": {"attachmentId": "789"},
                        }
                    ],
                },
            ]
        }
    }
    message.payload = data["payload"]

    with pytest.raises(MultipleAttachmentsError):
        message.get_attachment_metadata()


def test_message_with_body_attachment(message: Message):
    data = {"payload": {"filename": "file1.txt", "body": {"attachmentId": "123"}}}
    message.payload = data["payload"]
    attachment_id, filename = message.get_attachment_metadata()
    assert filename == "file1.txt"
    assert attachment_id == "123"


def test_message_with_no_attachment(message: Message):
    data = {"payload": {"headers": {"foo": "bar"}}}
    message.payload = data["payload"]

    with pytest.raises(AttachmentNotFoundError):
        message.get_attachment_metadata()

from monocloud.gmail import Message


def test_message_with_parts(message: Message):
    data = {
        "payload": {
            "parts": [
                {
                    "partId": "1",
                    "filename": "file1.txt",
                    "body": {"attachmentId": "123"},
                },
                {"partId": "2", "body": {"attachmentId": "456"}},
            ]
        }
    }
    message.payload = data["payload"]
    attachment_id, filename = message.get_attachment_metadata()
    assert filename == "file1.txt"
    assert attachment_id == "123"


def test_message_with_nested_parts(message: Message):
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
    attachment_id, filename = message.get_attachment_metadata()
    assert filename == "file1.txt"
    assert attachment_id == "123"


def test_message_with_no_parts(message: Message):
    data = {"payload": {"filename": "file1.txt", "body": {"attachmentId": "123"}}}
    message.payload = data["payload"]
    attachment_id, filename = message.get_attachment_metadata()
    assert filename == "file1.txt"
    assert attachment_id == "123"

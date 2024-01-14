from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from monocloud.config import cloud_settings
from monocloud.gmail.credentials import get_gmail_service

if TYPE_CHECKING:
    from googleapiclient._apis.gmail.v1.resources import GmailResource

logger = logging.getLogger("root")


def set_up_gmail_push_notifications():
    service: GmailResource = get_gmail_service()
    request_body = {
        "labelIds": ["INBOX"],
        "topicName": (
            f"projects/{cloud_settings.google_cloud_project}/"
            f"topics/{cloud_settings.pubsub_topic}"
        ),
    }

    # pylint: disable=no-member
    watch = (
        service.users()
        .watch(userId=cloud_settings.gmail_address, body=request_body)
        .execute()
    )

    logger.info(
        "Successfully set up watch request on inbox - historyId: %s", watch["historyId"]
    )

    return True


if __name__ == "__main__":
    set_up_gmail_push_notifications()

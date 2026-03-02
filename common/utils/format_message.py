import base64
import json

from common.schemas import ContentDlqSchema

list_dlqs = []


def formatting(msg):
    for item in msg:
        for key, value in item.items():
            topic = value.get("topic", "")
            for message in value.get("receivedMessages", []):
                content_dlq = ContentDlqSchema(
                    dlq=key,
                    topic=topic,
                    ackId=message.get("ackId"),
                    data=message.get("message", {}).get("data"),
                    publish_time=message.get("message", {}).get(
                        "publishTime"
                    ),
                    data_decoded=decode_data(
                        message.get("message", {}).get("data", "")
                    )
                )
                list_dlqs.append(content_dlq)

    return list_dlqs


def decode_data(data):
    return json.loads(base64.b64decode(data).decode("utf-8"))

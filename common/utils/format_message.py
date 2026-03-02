import base64
import json

list_dlqs = []
content_dlqs = {
    "dlq": "",
    "ackId": "",
    "data": "",
    "publishTime": "",
    "data_decoded": "",
    "topic": "",
}


def formatting(msg):
    for item in msg:
        for key, value in item.items():
            content_dlqs["dlq"] = key
            content_dlqs["topic"] = value.get("topic", "")
            for message in value.get("receivedMessages", []):
                content_dlqs["ackId"] = message.get("ackId")
                content_dlqs["data"] = message.get("message", {}).get("data")
                content_dlqs["publishTime"] = message.get("message", {}).get(
                    "publishTime"
                )
                content_dlqs["data_decoded"] = decode_data(
                    message.get("message", {}).get("data", "")
                )
                list_dlqs.append(content_dlqs.copy())

    return list_dlqs


def decode_data(data):
    return json.loads(base64.b64decode(data).decode("utf-8"))

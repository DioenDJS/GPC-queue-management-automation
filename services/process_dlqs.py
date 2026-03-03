import json
import logging

from agents.agent import call_agent
from common.utils.format_message import formatting
from common.utils.list_dlqs_and_topic import get_list_dlqs_and_topic
from helpers.api_google_cloud import GcpApi
from helpers.slack_channel_message import SlackChannelMessage

logger = logging.getLogger(__name__)

pubsub_api = GcpApi()
slack_service = SlackChannelMessage()


def process():
    list_dlqs_and_topic = get_list_dlqs_and_topic()
    list_dlq_and_topic_with_msgs = []

    for item in list_dlqs_and_topic:
        logger.info(f"running the subscription {item['subscription']}")
        response = pubsub_api.pubsub_subscription_pull(item["subscription"])
        response["topic"] = item["topic"]
        list_dlq_and_topic_with_msgs.append({item["subscription"]: response})

    list_dlq_and_topic_witch_msgs_decode = formatting(list_dlq_and_topic_with_msgs)

    for msg in list_dlq_and_topic_witch_msgs_decode:
        slack_service.send_to_message(msg)
        if msg.dlq in [
            "subscription-fila-um-dlq",
            "subscription-fila-quatro-dlq",
        ]:
            logs = pubsub_api.pubsub_entries_list(msg.publish_time)
            call_agent(
                json.dumps(
                    {"data_decoded": msg.data_decoded, "dlq": msg.dlq, "logs": logs},
                    ensure_ascii=False,
                )
            )
        pubsub_api.pubsub_topics_publish(topic=msg.topic, message=msg.data)
        pubsub_api.pubsub_subscription_acknowledge(
            subscription=msg.dlq, ack_ids=[msg.ackId]
        )

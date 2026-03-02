from helpers.api_google_cloud import GcpApi
from common.utils.list_dlqs_and_topic import get_list_dlqs_and_topic

pubsub_api = GcpApi()

def process():
    list_dlqs_and_topic = get_list_dlqs_and_topic()

    for item in list_dlqs_and_topic:
        response = pubsub_api.pubsub_subscription_pull(item["subscription"])
        print(response)

    
import logging
import os

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
logger = logging.getLogger(__name__)


class SlackChannelMessage:
    def __init__(self):
        self.client = WebClient(token=os.getenv("SLACK_CLIENT_TOKEN"))
        self.channel_id = os.getenv("SLACK_CHANNAL_ID")

    def send_to_message(self, msg_dlq, agent=False):
        try:
            text = f":clipboard: DLQ:{msg_dlq.get('dlq', '')} \n:clock3: PublishTime:{msg_dlq.get('publishTime', '')}\n\n"

            if agent:
                text = f"🚨 *Alerta de DLQ*: {msg_dlq.get('dlq', '')} 🚨\n"
                text += f"{msg_dlq.get('content', '')}\n"
            else:
                text = f":clipboard: DLQ:{msg_dlq.get('dlq', '')} \n:clock3: PublishTime:{msg_dlq.get('publishTime', '')}\n\n"
                text += f"{msg_dlq.get('data_decoded', '')}\n"
            response = self.client.chat_postMessage(
                channel=self.channel_id,
                text=text,
                blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": text}}],
            )
            return response
        except SlackApiError as e:
            logger.error(f"Erro ao enviar para o Slack: {e.response['error']}")
            raise

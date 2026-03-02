import logging

import google.auth
import requests
from google.auth.transport.requests import Request

from common.config.settings import settings

logger = logging.getLogger(__name__)


class GcpApi:
    def __init__(self):
        self.base_url = settings.base_url_pubsub
        self.credentials, self.project_id = google.auth.default(
            scopes=[settings.scopes_pubsub]
        )

    def _get_access_token(self):
        if not self.credentials.valid:
            self.credentials.refresh(Request())
        return self.credentials.token

    def pubsub_subscription_pull(self, subscription):
        url = f"{self.base_url}subscriptions/{subscription}:pull"

        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-type": "application/json",
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json={"maxMessages": 10, "returnImmediately": True},
                timeout=15,
            )

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f"HTTP error when pulling subscription messages {subscription}"
            )
            if response.status_code == 401:
                logger.warning(
                    "Tip: Check if your Google Cloud token has expired or is invalid."
                )
                return None
        except Exception as e:
            logger.exception(f"Unexpected error in PubSub Pull for{subscription}")
            raise

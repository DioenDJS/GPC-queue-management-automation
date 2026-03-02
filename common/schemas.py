from pydantic import BaseModel
from typing import Any

class ContentDlqSchema(BaseModel):
    dlq: str
    ackId: str
    data: str
    publish_time: str
    data_decoded: dict[str, Any]
    topic: str

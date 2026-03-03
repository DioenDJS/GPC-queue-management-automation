from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url_pubsub: str = (
        "https://pubsub.googleapis.com/v1/projects/integracaon8n-486515/"
    )
    scopes_pubsub: str = "https://www.googleapis.com/auth/pubsub"
    project_id: str = "integracaon8n-486515"


settings = Settings()

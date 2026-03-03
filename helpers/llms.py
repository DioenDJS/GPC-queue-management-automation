import os
from enum import Enum

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()


class LLMProvider(str, Enum):
    OLLAMA_GLM_5_CLOUD = "ollama_glm_5_cloud"
    OLLAMA_GLM_4_7_CLOUD = "ollama_glm_4_7_cloud"


class Llms:
    def __init__(self, provider: LLMProvider, temperature: float = 0.1):
        self.provider = provider
        self.temperature = temperature
        self._llm = None

    def get_llm(self):
        if self._llm is None:
            self._llm = self._build_llm()
        return self._llm

    def _build_llm(self):
        if self.provider == LLMProvider.OLLAMA_GLM_4_7_CLOUD:
            return ChatOllama(
                model=os.getenv("OLLAMA_GLM_4_7_C"), temperature=self.temperature
            )
        elif self.provider == LLMProvider.OLLAMA_GLM_5_CLOUD:
            return ChatOllama(
                model=os.getenv("OLLAMA_GLM_5_C"), temperature=self.temperature
            )
        else:
            raise ValueError(f"Provider '{self.provider}' not found!")

from abc import ABC, abstractmethod
from typing import Generator
from django.conf import settings


class AIProvider(ABC):
    @abstractmethod
    def stream(self, messages: list) -> Generator[str, None, None]:
        ...

    @abstractmethod
    def complete(self, messages: list) -> str:
        ...


class OpenAIProvider(AIProvider):
    MODEL = 'gpt-4o-mini'

    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def stream(self, messages: list) -> Generator[str, None, None]:
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
            stream=True,
            temperature=0.7,
            max_tokens=1000,
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content

    def complete(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content


class AIProviderFactory:
    @staticmethod
    def get() -> AIProvider:
        provider_name = getattr(settings, 'AI_PROVIDER', 'openai')
        if provider_name == 'openai':
            return OpenAIProvider()
        raise ValueError(f"Неизвестный AI провайдер: {provider_name}")

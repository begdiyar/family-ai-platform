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

    def __init__(self):
        import openai
        import httpx
        self.model = getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini')
        self.client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY,
            http_client=httpx.Client(),
        )

    def _tokens_kwarg(self, n: int) -> dict:
        if self.model.startswith('gpt-5'):
            # openai==1.30.5 SDK doesn't accept max_completion_tokens as a named param;
            # extra_body injects it directly into the JSON request body, bypassing SDK validation
            return {'extra_body': {'max_completion_tokens': n}}
        return {'max_tokens': n}

    def stream(self, messages: list) -> Generator[str, None, None]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            temperature=0.7,
            **self._tokens_kwarg(1000),
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content

    def complete(self, messages: list, max_tokens: int = 3000) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            **self._tokens_kwarg(max_tokens),
        )
        return response.choices[0].message.content


class AIProviderFactory:
    @staticmethod
    def get() -> AIProvider:
        provider_name = getattr(settings, 'AI_PROVIDER', 'openai')
        if provider_name == 'openai':
            return OpenAIProvider()
        raise ValueError(f"Неизвестный AI провайдер: {provider_name}")

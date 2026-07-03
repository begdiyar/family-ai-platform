from django.conf import settings

from .base import AIProvider


class AIProviderFactory:

    @staticmethod
    def get() -> AIProvider:
        provider_name = getattr(settings, 'AI_PROVIDER', 'openai')
        if provider_name == 'openai':
            from .openai import OpenAIProvider
            return OpenAIProvider()
        raise ValueError(f'Неизвестный AI провайдер: {provider_name}')

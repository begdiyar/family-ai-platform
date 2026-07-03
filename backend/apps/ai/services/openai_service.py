import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    DEFAULT_MODEL = 'gpt-4o-mini'

    def __init__(self):
        try:
            import openai as _openai
            self._openai = _openai
        except ImportError:
            raise RuntimeError('openai пакет не установлен: pip install openai')

        api_key = getattr(settings, 'OPENAI_API_KEY', '')
        if not api_key:
            raise ValueError('OPENAI_API_KEY не задан в настройках (.env)')

        import httpx
        self.model  = getattr(settings, 'OPENAI_MODEL', self.DEFAULT_MODEL)
        self.client = self._openai.OpenAI(api_key=api_key, http_client=httpx.Client())

    def _tokens_kwarg(self, n: int) -> dict:
        if self.model.startswith('gpt-5'):
            # openai==1.30.5 SDK doesn't accept max_completion_tokens as a named param;
            # extra_body injects it directly into the JSON request body, bypassing SDK validation
            return {'extra_body': {'max_completion_tokens': n}}
        return {'max_tokens': n}

    def generate_response(
        self,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Отправляет список messages в OpenAI и возвращает текст ответа.
        messages — стандартный формат: [{"role": "system"|"user"|"assistant", "content": "..."}]
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                **self._tokens_kwarg(max_tokens),
            )
            return (response.choices[0].message.content or '').strip()
        except self._openai.AuthenticationError as e:
            logger.error('OpenAI authentication failed: %s', e)
            raise ValueError('Неверный OPENAI_API_KEY') from e
        except self._openai.RateLimitError as e:
            logger.warning('OpenAI rate limit hit: %s', e)
            raise RuntimeError('Превышен лимит запросов OpenAI. Попробуйте позже.') from e
        except self._openai.APIConnectionError as e:
            logger.error('OpenAI connection error: %s', e)
            raise RuntimeError('Нет соединения с OpenAI API.') from e
        except Exception as e:
            logger.error('OpenAI unexpected error: %s', e, exc_info=True)
            raise

import secrets
import string
from django.utils import timezone
from datetime import timedelta

SUPPORTED_LANGUAGES = {'ru', 'en', 'uz'}


def generate_token(length: int = 48) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def future_datetime(hours: int = 0, days: int = 0):
    return timezone.now() + timedelta(hours=hours, days=days)


def get_request_language(request) -> str:
    lang = (
        request.headers.get('X-Language')
        or request.META.get('HTTP_X_LANGUAGE')
        or (
            getattr(request.user, 'preferred_language', None)
            if hasattr(request, 'user') and getattr(request.user, 'is_authenticated', False)
            else None
        )
        or 'ru'
    )
    return lang if lang in SUPPORTED_LANGUAGES else 'ru'


def get_i18n(obj, field: str, lang: str) -> str:
    """Return translated field value, falling back to main field (Russian)."""
    if lang == 'ru':
        return getattr(obj, field, '')
    translations = getattr(obj, 'i18n', {}) or {}
    return translations.get(lang, {}).get(field) or getattr(obj, field, '')

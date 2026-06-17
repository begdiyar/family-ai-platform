from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """Единый формат ответа: всегда возвращает корректный JSON без BOM."""
    charset = 'utf-8'

from rest_framework import serializers
from .models import AnalyticsResult, AnalyticsInsight


class AnalyticsResultShortSerializer(serializers.ModelSerializer):
    is_latest    = serializers.SerializerMethodField()
    level_number = serializers.SerializerMethodField()

    def get_is_latest(self, obj):
        return self.context.get('latest_id') == str(obj.id)

    def get_level_number(self, obj):
        try:
            return obj.session_a.level_number
        except Exception:
            return 1

    class Meta:
        model = AnalyticsResult
        fields = ['id', 'overall_score', 'is_latest', 'level_number', 'created_at']


class ZoneScoreDetailSerializer(serializers.Serializer):
    zone = serializers.CharField()
    label = serializers.CharField()
    partner_a = serializers.DictField()
    partner_b = serializers.DictField()
    couple_avg = serializers.FloatField()
    gap = serializers.FloatField()
    status = serializers.CharField()


def _resolve_lang(context) -> str:
    request = context.get('request')
    if not request:
        return 'ru'
    header = (request.headers.get('X-Language') or '').lower()
    if header in ('ru', 'en', 'uz'):
        return header
    if hasattr(request, 'user') and request.user.is_authenticated:
        return getattr(request.user, 'preferred_language', None) or 'ru'
    return 'ru'


def _pick(value, lang: str):
    """Return language-specific text from a multilang dict, falling back to 'ru'."""
    if not isinstance(value, dict):
        return value  # legacy plain string — return as-is
    return value.get(lang) or value.get('ru') or ''


def _pick_json(value, lang: str):
    """Return language-specific JSON (dict/list) from a multilang wrapper, falling back to 'ru'."""
    if not isinstance(value, dict):
        return value  # legacy structure — return as-is
    # New structure: {"ru": {...}, "en": {...}, "uz": {...}}
    if 'ru' in value or 'en' in value or 'uz' in value:
        return value.get(lang) or value.get('ru')
    # Old structure without language keys — return as-is
    return value


class AnalyticsResultDetailSerializer(serializers.ModelSerializer):
    zone_scores = serializers.SerializerMethodField()
    strengths = serializers.SerializerMethodField()
    attention_zones = serializers.SerializerMethodField()

    def _get_zones(self, obj):
        cache_key = f'_zones_{obj.id}'
        if cache_key not in self.context:
            from .services import AnalyticsService
            self.context[cache_key] = AnalyticsService.get_zone_detail_for_result(obj)
        return self.context[cache_key]

    def get_zone_scores(self, obj):
        return ZoneScoreDetailSerializer(self._get_zones(obj), many=True).data

    def get_strengths(self, obj):
        return [z['zone'] for z in self._get_zones(obj) if z['status'] == 'strong']

    def get_attention_zones(self, obj):
        return [z['zone'] for z in self._get_zones(obj) if z['status'] == 'attention']

    level_number = serializers.SerializerMethodField()

    def get_level_number(self, obj):
        try:
            return obj.session_a.level_number
        except Exception:
            return 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = _resolve_lang(self.context)
        data['bridge_analysis'] = _pick_json(data.get('bridge_analysis'), lang)
        data['strengths_summary'] = _pick_json(data.get('strengths_summary'), lang)
        data['problem_chain'] = _pick_json(data.get('problem_chain'), lang)
        data['key_insights'] = _pick_json(data.get('key_insights'), lang)
        return data

    class Meta:
        model = AnalyticsResult
        fields = ['id', 'overall_score', 'zone_scores', 'strengths', 'attention_zones',
                  'key_insights', 'crisis_level', 'bridge_analysis', 'strengths_summary',
                  'problem_chain', 'relatives_index', 'finance_index',
                  'child_environment_index', 'level_number', 'created_at']


class AnalyticsInsightSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = _resolve_lang(self.context)
        for field in ['strengths_summary', 'growth_summary', 'attention_summary', 'ai_analysis', 'recommendation', 'next_focus']:
            data[field] = _pick(data[field], lang)
        return data

    class Meta:
        model = AnalyticsInsight
        fields = [
            'id', 'strengths_summary', 'growth_summary', 'attention_summary',
            'ai_analysis', 'recommendation', 'next_focus', 'created_at',
        ]


class ProgressHistorySerializer(serializers.Serializer):
    date = serializers.DateTimeField(source='created_at')
    result_id = serializers.UUIDField(source='id')
    scores = serializers.SerializerMethodField()

    def get_scores(self, obj):
        from .services import AnalyticsService
        zones = AnalyticsService.get_zone_detail_for_result(obj)
        return {z['zone']: z['couple_avg'] for z in zones}

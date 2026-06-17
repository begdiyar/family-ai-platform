from rest_framework import serializers
from .models import AnalyticsResult


class AnalyticsResultShortSerializer(serializers.ModelSerializer):
    is_latest = serializers.SerializerMethodField()

    def get_is_latest(self, obj):
        return self.context.get('latest_id') == str(obj.id)

    class Meta:
        model = AnalyticsResult
        fields = ['id', 'overall_score', 'is_latest', 'created_at']


class ZoneScoreDetailSerializer(serializers.Serializer):
    zone = serializers.CharField()
    label = serializers.CharField()
    partner_a = serializers.DictField()
    partner_b = serializers.DictField()
    couple_avg = serializers.FloatField()
    gap = serializers.FloatField()
    status = serializers.CharField()


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

    class Meta:
        model = AnalyticsResult
        fields = ['id', 'overall_score', 'zone_scores', 'strengths', 'attention_zones',
                  'key_insights', 'crisis_level', 'bridge_analysis', 'strengths_summary',
                  'problem_chain', 'relatives_index', 'finance_index',
                  'child_environment_index', 'created_at']


class ProgressHistorySerializer(serializers.Serializer):
    date = serializers.DateTimeField(source='created_at')
    result_id = serializers.UUIDField(source='id')
    scores = serializers.SerializerMethodField()

    def get_scores(self, obj):
        from .services import AnalyticsService
        zones = AnalyticsService.get_zone_detail_for_result(obj)
        return {z['zone']: z['couple_avg'] for z in zones}

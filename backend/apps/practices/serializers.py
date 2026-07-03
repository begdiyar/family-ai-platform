from rest_framework import serializers
from .models import (
    Practice, DailyAssignment, AssignmentSlot, FamilyDevelopmentPlan,
    SLOT_ORDER, FAMILY_LEVELS, STAGE_BY_LEVEL,
)


def _localize(practice: Practice, field: str, lang: str) -> str:
    if lang and lang != 'ru' and practice.i18n:
        translated = (practice.i18n.get(lang) or {}).get(field)
        if translated:
            return translated
    return getattr(practice, field, '')


class PracticeSerializer(serializers.ModelSerializer):
    title                = serializers.SerializerMethodField()
    description          = serializers.SerializerMethodField()
    instructions         = serializers.SerializerMethodField()
    category_label       = serializers.CharField(source='get_category_display', read_only=True)
    slot_label           = serializers.CharField(source='get_slot_type_display', read_only=True)
    difficulty_label     = serializers.CharField(source='get_difficulty_display', read_only=True)
    academy_article_slug = serializers.SerializerMethodField()

    def get_title(self, obj):
        return _localize(obj, 'title', self.context.get('lang', 'ru'))

    def get_description(self, obj):
        return _localize(obj, 'description', self.context.get('lang', 'ru'))

    def get_instructions(self, obj):
        return _localize(obj, 'instructions', self.context.get('lang', 'ru'))

    def get_academy_article_slug(self, obj):
        if obj.academy_article_id:
            return obj.academy_article.slug
        return None

    class Meta:
        model  = Practice
        fields = [
            'id', 'title', 'description', 'instructions',
            'category', 'category_label',
            'slot_type', 'slot_label',
            'difficulty', 'difficulty_label',
            'duration_minutes', 'tags',
            'academy_article_slug',
        ]


class AssignmentSlotSerializer(serializers.ModelSerializer):
    practice   = serializers.SerializerMethodField()
    slot_label = serializers.CharField(source='get_slot_type_display', read_only=True)

    def get_practice(self, obj):
        if obj.practice is None:
            return None
        return PracticeSerializer(obj.practice, context=self.context).data

    class Meta:
        model  = AssignmentSlot
        fields = ['slot_type', 'slot_label', 'practice', 'completed', 'completed_at']


class FamilyDevelopmentPlanSerializer(serializers.ModelSerializer):
    stage_name          = serializers.SerializerMethodField()
    stage_emoji         = serializers.SerializerMethodField()
    level_label         = serializers.SerializerMethodField()
    level_emoji         = serializers.SerializerMethodField()
    level_xp_current    = serializers.SerializerMethodField()
    level_xp_for_next   = serializers.SerializerMethodField()
    level_progress_pct  = serializers.SerializerMethodField()
    next_diagnostic_in_days = serializers.SerializerMethodField()
    requires_diagnostic = serializers.SerializerMethodField()

    def _level_row(self, obj):
        for row in FAMILY_LEVELS:
            if row[2] == obj.current_level:
                return row
        return FAMILY_LEVELS[-1]

    def get_stage_name(self, obj):
        return STAGE_BY_LEVEL.get(obj.current_level, (1, 'Восстановление связи', '🌱'))[1]

    def get_stage_emoji(self, obj):
        return STAGE_BY_LEVEL.get(obj.current_level, (1, 'Восстановление связи', '🌱'))[2]

    def get_level_label(self, obj):
        return self._level_row(obj)[3]

    def get_level_emoji(self, obj):
        return self._level_row(obj)[4]

    def get_level_xp_current(self, obj):
        min_v = self._level_row(obj)[0]
        return max(0, obj.total_completed - min_v)

    def get_level_xp_for_next(self, obj):
        min_v, max_v = self._level_row(obj)[0], self._level_row(obj)[1]
        return 0 if max_v >= 9999 else (max_v - min_v + 1)

    def get_level_progress_pct(self, obj):
        min_v, max_v = self._level_row(obj)[0], self._level_row(obj)[1]
        if max_v >= 9999:
            return 100
        span = max_v - min_v + 1
        return round(max(0, obj.total_completed - min_v) / span * 100)

    def get_next_diagnostic_in_days(self, obj):
        if not obj.next_diagnostic_at:
            return None
        from django.utils import timezone
        delta = obj.next_diagnostic_at - timezone.now()
        return max(0, delta.days)

    def get_requires_diagnostic(self, obj):
        if not obj.next_diagnostic_at:
            return False
        from django.utils import timezone
        return timezone.now() >= obj.next_diagnostic_at

    class Meta:
        model  = FamilyDevelopmentPlan
        fields = [
            'id',
            'current_level', 'current_stage',
            'stage_name', 'stage_emoji',
            'level_label', 'level_emoji',
            'level_xp_current', 'level_xp_for_next', 'level_progress_pct',
            'priority_zone', 'secondary_zone', 'tertiary_zone',
            'total_completed',
            'next_diagnostic_in_days', 'requires_diagnostic',
            'last_diagnostic_at',
        ]


class DailyAssignmentSerializer(serializers.ModelSerializer):
    slots              = serializers.SerializerMethodField()
    completed_count    = serializers.IntegerField(read_only=True)
    total_completable  = serializers.IntegerField(read_only=True)
    is_fully_completed = serializers.BooleanField(read_only=True)
    is_ai_generated    = serializers.SerializerMethodField()
    plan               = serializers.SerializerMethodField()

    def get_slots(self, obj):
        slot_map = {s.slot_type: s for s in obj.slots.all()}
        result   = []
        for slot_type in SLOT_ORDER:
            slot = slot_map.get(slot_type)
            if slot:
                result.append(AssignmentSlotSerializer(slot, context=self.context).data)
        return result

    def get_is_ai_generated(self, obj):
        return obj.is_ai_generated

    def get_plan(self, _obj):
        plan = self.context.get('plan')
        if plan is None:
            return None
        return FamilyDevelopmentPlanSerializer(plan).data

    class Meta:
        model  = DailyAssignment
        fields = [
            'id', 'date', 'slots',
            'completed_count', 'total_completable', 'is_fully_completed',
            'categories_used', 'is_ai_generated', 'plan',
        ]

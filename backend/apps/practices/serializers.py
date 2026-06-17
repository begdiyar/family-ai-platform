from rest_framework import serializers
from shared.utils import get_i18n
from .models import DailyPractice

PRACTICE_FIELDS = [
    'question_of_day', 'conversation_topic', 'trust_exercise',
    'communication_exercise', 'family_activity', 'romantic_idea',
]


class DailyPracticeSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        completions = self.context.get('completions', set())
        lang = self.context.get('language', 'ru')
        return [
            {
                'key': field,
                'content': get_i18n(obj, field, lang),
                'completed': field in completions,
            }
            for field in PRACTICE_FIELDS
        ]

    class Meta:
        model = DailyPractice
        fields = ['id', 'date', 'is_ai_generated', 'items']

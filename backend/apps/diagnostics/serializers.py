from rest_framework import serializers
from .models import Question, DiagnosticSession
from .repositories import DiagnosticRepository, QuestionRepository

SUPPORTED_LANGS = ('ru', 'en', 'uz')


def _lang(request) -> str:
    lang = (request.headers.get('X-Language') or 'ru').lower()
    return lang if lang in SUPPORTED_LANGS else 'ru'


class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    def get_text(self, obj):
        request = self.context.get('request')
        if request:
            lang = _lang(request)
            if lang != 'ru' and obj.i18n.get(lang, {}).get('text'):
                return obj.i18n[lang]['text']
        return obj.text

    class Meta:
        model = Question
        fields = ['id', 'zone', 'level_number', 'text', 'question_type', 'options', 'order_index']


class SessionSerializer(serializers.ModelSerializer):
    answers_count = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    def get_answers_count(self, obj):
        return DiagnosticRepository.get_answers_count(obj)

    def get_total_questions(self, obj):
        return QuestionRepository.count_by_level(obj.level_number)

    def get_progress_percent(self, obj):
        count = DiagnosticRepository.get_answers_count(obj)
        total = QuestionRepository.count_by_level(obj.level_number)
        return round(count / total * 100) if total else 0

    class Meta:
        model = DiagnosticSession
        fields = [
            'id', 'status', 'level_number',
            'started_at', 'finished_at',
            'answers_count', 'total_questions', 'progress_percent',
        ]


class AnswerInputSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    value_scale = serializers.IntegerField(min_value=1, max_value=5, required=False, allow_null=True)
    value_choice = serializers.CharField(max_length=100, required=False, allow_null=True)
    value_text = serializers.CharField(required=False, allow_null=True)


class SaveAnswersSerializer(serializers.Serializer):
    answers = AnswerInputSerializer(many=True)


class StartSessionSerializer(serializers.Serializer):
    level_number = serializers.IntegerField(min_value=1, max_value=10, default=1)

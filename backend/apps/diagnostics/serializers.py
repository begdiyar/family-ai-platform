from rest_framework import serializers
from .models import Question, DiagnosticSession


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'zone', 'text', 'question_type', 'options', 'order_index']


class ZoneQuestionsSerializer(serializers.Serializer):
    zone = serializers.CharField()
    label = serializers.CharField()
    questions = QuestionSerializer(many=True)


class SessionSerializer(serializers.ModelSerializer):
    answers_count = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    def get_answers_count(self, obj):
        from .repositories import DiagnosticRepository
        return DiagnosticRepository.get_answers_count(obj)

    def get_total_questions(self, obj):
        from .repositories import QuestionRepository
        return QuestionRepository.count_active()

    def get_progress_percent(self, obj):
        from .repositories import DiagnosticRepository, QuestionRepository
        count = DiagnosticRepository.get_answers_count(obj)
        total = QuestionRepository.count_active()
        return round(count / total * 100) if total else 0

    class Meta:
        model = DiagnosticSession
        fields = ['id', 'status', 'started_at', 'finished_at',
                  'answers_count', 'total_questions', 'progress_percent']


class AnswerInputSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    value_scale = serializers.IntegerField(min_value=1, max_value=5, required=False, allow_null=True)
    value_choice = serializers.CharField(max_length=100, required=False, allow_null=True)
    value_text = serializers.CharField(required=False, allow_null=True)


class SaveAnswersSerializer(serializers.Serializer):
    answers = AnswerInputSerializer(many=True)

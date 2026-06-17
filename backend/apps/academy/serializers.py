from rest_framework import serializers
from shared.utils import get_i18n
from .models import (
    ArticleSource, Article, Training, Program, ProgramDay,
    AcademyMicroPractice, UserTrainingProgress, UserProgramEnrollment,
    UserAchievement, Achievement,
)


class ArticleSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleSource
        fields = ['name', 'source_type', 'trust_level', 'url']


class ArticleListSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    brief = serializers.SerializerMethodField()

    def _lang(self):
        return self.context.get('language', 'ru')

    def get_is_completed(self, obj):
        completed_ids = self.context.get('completed_ids', set())
        return str(obj.id) in completed_ids

    def get_title(self, obj):
        return get_i18n(obj, 'title', self._lang())

    def get_brief(self, obj):
        return get_i18n(obj, 'brief', self._lang())

    class Meta:
        model = Article
        fields = [
            'id', 'slug', 'category', 'title', 'brief',
            'read_time_minutes', 'difficulty', 'tags', 'is_completed', 'order_index',
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    sources = ArticleSourceSerializer(many=True, read_only=True)
    is_completed = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    brief = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    def _lang(self):
        return self.context.get('language', 'ru')

    def get_is_completed(self, obj):
        completed_ids = self.context.get('completed_ids', set())
        return str(obj.id) in completed_ids

    def get_title(self, obj):
        return get_i18n(obj, 'title', self._lang())

    def get_brief(self, obj):
        return get_i18n(obj, 'brief', self._lang())

    def get_body(self, obj):
        return get_i18n(obj, 'body', self._lang())

    class Meta:
        model = Article
        fields = [
            'id', 'slug', 'category', 'title', 'brief', 'body',
            'read_time_minutes', 'difficulty', 'tags', 'sources', 'is_completed',
        ]


class TrainingListSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def _lang(self):
        return self.context.get('language', 'ru')

    def get_is_completed(self, obj):
        prog = self.context.get('training_progress', {}).get(str(obj.id))
        return prog is not None and prog.status == UserTrainingProgress.STATUS_COMPLETED

    def get_status(self, obj):
        prog = self.context.get('training_progress', {}).get(str(obj.id))
        if prog is None:
            return 'not_started'
        return prog.status

    def get_title(self, obj):
        return get_i18n(obj, 'title', self._lang())

    def get_description(self, obj):
        return get_i18n(obj, 'description', self._lang())

    class Meta:
        model = Training
        fields = [
            'id', 'slug', 'skill_type', 'title', 'description',
            'duration_minutes', 'difficulty', 'is_completed', 'status', 'order_index',
        ]


class TrainingDetailSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    reflection_note = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    theory = serializers.SerializerMethodField()
    exercise_instruction = serializers.SerializerMethodField()
    completion_check = serializers.SerializerMethodField()

    def _lang(self):
        return self.context.get('language', 'ru')

    def get_is_completed(self, obj):
        prog = self.context.get('progress')
        return prog is not None and prog.status == UserTrainingProgress.STATUS_COMPLETED

    def get_status(self, obj):
        prog = self.context.get('progress')
        if prog is None:
            return 'not_started'
        return prog.status

    def get_reflection_note(self, obj):
        prog = self.context.get('progress')
        return prog.reflection_note if prog else None

    def get_title(self, obj):
        return get_i18n(obj, 'title', self._lang())

    def get_description(self, obj):
        return get_i18n(obj, 'description', self._lang())

    def get_theory(self, obj):
        return get_i18n(obj, 'theory', self._lang())

    def get_exercise_instruction(self, obj):
        return get_i18n(obj, 'exercise_instruction', self._lang())

    def get_completion_check(self, obj):
        return get_i18n(obj, 'completion_check', self._lang())

    class Meta:
        model = Training
        fields = [
            'id', 'slug', 'skill_type', 'title', 'description',
            'theory', 'exercise_instruction', 'completion_check',
            'duration_minutes', 'difficulty', 'is_completed', 'status', 'reflection_note',
        ]


class ProgramDaySerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    material = serializers.SerializerMethodField()
    exercise = serializers.SerializerMethodField()
    reflection_prompt = serializers.SerializerMethodField()

    def _lang(self):
        return self.context.get('language', 'ru')

    def get_is_completed(self, obj):
        completed_days = self.context.get('completed_days', set())
        return obj.day_number in completed_days

    def get_title(self, obj):
        return get_i18n(obj, 'title', self._lang())

    def get_material(self, obj):
        return get_i18n(obj, 'material', self._lang())

    def get_exercise(self, obj):
        return get_i18n(obj, 'exercise', self._lang())

    def get_reflection_prompt(self, obj):
        return get_i18n(obj, 'reflection_prompt', self._lang())

    class Meta:
        model = ProgramDay
        fields = ['id', 'day_number', 'title', 'material', 'exercise', 'reflection_prompt', 'is_completed']


class ProgramListSerializer(serializers.ModelSerializer):
    is_enrolled = serializers.SerializerMethodField()
    enrollment_status = serializers.SerializerMethodField()
    current_day = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def _lang(self):
        return self.context.get('language', 'ru')

    def _get_enrollment(self, obj):
        enrollments = self.context.get('enrollments', {})
        return enrollments.get(str(obj.id))

    def get_title(self, obj):
        return get_i18n(obj, 'title', self._lang())

    def get_description(self, obj):
        return get_i18n(obj, 'description', self._lang())

    def get_is_enrolled(self, obj):
        return self._get_enrollment(obj) is not None

    def get_enrollment_status(self, obj):
        e = self._get_enrollment(obj)
        return e.status if e else 'not_enrolled'

    def get_current_day(self, obj):
        e = self._get_enrollment(obj)
        return e.current_day if e else 0

    def get_progress_percent(self, obj):
        e = self._get_enrollment(obj)
        if not e:
            return 0
        return round(e.current_day / obj.duration_days * 100)

    class Meta:
        model = Program
        fields = [
            'id', 'slug', 'title', 'description', 'duration_days',
            'category_focus', 'cover_gradient', 'is_enrolled',
            'enrollment_status', 'current_day', 'progress_percent', 'order_index',
        ]


class ProgramDetailSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    enrollment_status = serializers.SerializerMethodField()
    current_day = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def _lang(self):
        return self.context.get('language', 'ru')

    def _get_enrollment(self, obj):
        return self.context.get('enrollment')

    def get_title(self, obj):
        return get_i18n(obj, 'title', self._lang())

    def get_description(self, obj):
        return get_i18n(obj, 'description', self._lang())

    def get_is_enrolled(self, obj):
        return self._get_enrollment(obj) is not None

    def get_enrollment_status(self, obj):
        e = self._get_enrollment(obj)
        return e.status if e else 'not_enrolled'

    def get_current_day(self, obj):
        e = self._get_enrollment(obj)
        return e.current_day if e else 0

    def get_progress_percent(self, obj):
        e = self._get_enrollment(obj)
        if not e:
            return 0
        return round(e.current_day / obj.duration_days * 100)

    def get_days(self, obj):
        completed_days = self.context.get('completed_days', set())
        return ProgramDaySerializer(
            obj.days.all(), many=True,
            context={'completed_days': completed_days, 'language': self._lang()}
        ).data

    class Meta:
        model = Program
        fields = [
            'id', 'slug', 'title', 'description', 'duration_days',
            'category_focus', 'cover_gradient', 'days',
            'is_enrolled', 'enrollment_status', 'current_day', 'progress_percent',
        ]


class MicroPracticeSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    instruction = serializers.SerializerMethodField()

    def _lang(self):
        return self.context.get('language', 'ru')

    def get_is_completed(self, obj):
        return self.context.get('is_completed', False)

    def get_title(self, obj):
        return get_i18n(obj, 'title', self._lang())

    def get_instruction(self, obj):
        return get_i18n(obj, 'instruction', self._lang())

    class Meta:
        model = AcademyMicroPractice
        fields = ['id', 'title', 'instruction', 'category', 'duration_minutes', 'is_completed']


class LearningProgressSerializer(serializers.Serializer):
    articles_read = serializers.IntegerField()
    trainings_completed = serializers.IntegerField()
    programs_completed = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    total_minutes = serializers.IntegerField()
    skills = serializers.ListField(child=serializers.DictField())


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'key', 'title', 'description', 'icon', 'condition_type', 'condition_value']


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ['achievement', 'earned_at']


class ReflectSerializer(serializers.Serializer):
    question_key = serializers.ChoiceField(choices=['understood', 'try', 'apply'])
    answer = serializers.CharField(max_length=2000)


class CompleteTrainingSerializer(serializers.Serializer):
    reflection_note = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class CompleteDaySerializer(serializers.Serializer):
    reflection = serializers.CharField(required=False, allow_blank=True, allow_null=True)

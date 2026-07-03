from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shared.exceptions import NotFoundError, ConflictError
from shared.utils import get_request_language

from .repositories import (
    ArticleRepository, TrainingRepository, ProgramRepository,
    MicroPracticeRepository, AchievementRepository,
)
from .services import AcademyService
from .serializers import (
    ArticleListSerializer, ArticleDetailSerializer,
    TrainingListSerializer, TrainingDetailSerializer,
    ProgramListSerializer, ProgramDetailSerializer,
    MicroPracticeSerializer, LearningProgressSerializer,
    UserAchievementSerializer, ReflectSerializer,
    CompleteTrainingSerializer, CompleteDaySerializer,
)


# ── Articles ──────────────────────────────────────────────────────────────────

class ArticleListView(APIView):
    def get(self, request):
        category = request.query_params.get('category')
        difficulty = request.query_params.get('difficulty')
        search = request.query_params.get('search')
        lang = get_request_language(request)
        articles = ArticleRepository.list_published(category=category, difficulty=difficulty, search=search)
        completed_ids = ArticleRepository.get_completed_ids_for_user(request.user)
        serializer = ArticleListSerializer(
            articles, many=True, context={'completed_ids': completed_ids, 'language': lang}
        )
        return Response({'count': len(serializer.data), 'results': serializer.data})


class ArticleDetailView(APIView):
    def get(self, request, slug):
        article = ArticleRepository.get_by_slug(slug)
        if not article:
            raise NotFoundError('ARTICLE_NOT_FOUND', 'Статья не найдена')
        lang = get_request_language(request)
        completed_ids = ArticleRepository.get_completed_ids_for_user(request.user)
        return Response(ArticleDetailSerializer(
            article, context={'completed_ids': completed_ids, 'language': lang}
        ).data)


class ArticleCompleteView(APIView):
    def post(self, request, slug):
        article = ArticleRepository.get_by_slug(slug)
        if not article:
            raise NotFoundError('ARTICLE_NOT_FOUND', 'Статья не найдена')
        created = ArticleRepository.mark_complete(request.user, article)
        if created:
            AcademyService.check_and_award_achievements(request.user)
        return Response({'completed': True, 'newly_completed': created})


class ArticleReflectView(APIView):
    def post(self, request, slug):
        article = ArticleRepository.get_by_slug(slug)
        if not article:
            raise NotFoundError('ARTICLE_NOT_FOUND', 'Статья не найдена')
        serializer = ReflectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question_key = serializer.validated_data['question_key']
        answer = serializer.validated_data['answer']

        QUESTIONS = {
            'understood': 'Что вы поняли из этой статьи?',
            'try': 'Что хотите попробовать?',
            'apply': 'Как применить это в вашей семье?',
        }
        NEXT_QUESTIONS = {
            'understood': 'try',
            'try': 'apply',
            'apply': None,
        }

        ai_response = f'Отлично! Вы ответили: «{answer}». Это ценное осознание. '
        next_key = NEXT_QUESTIONS.get(question_key)
        next_question = QUESTIONS.get(next_key) if next_key else None

        return Response({
            'question_key': question_key,
            'answer': answer,
            'ai_response': ai_response,
            'next_question_key': next_key,
            'next_question': next_question,
        })


# ── Trainings ─────────────────────────────────────────────────────────────────

class TrainingListView(APIView):
    def get(self, request):
        lang = get_request_language(request)
        trainings = TrainingRepository.list_all()
        progress_map = TrainingRepository.get_all_progress_for_user(request.user)
        serializer = TrainingListSerializer(
            trainings, many=True, context={'training_progress': progress_map, 'language': lang}
        )
        return Response({'count': len(serializer.data), 'results': serializer.data})


class TrainingDetailView(APIView):
    def get(self, request, slug):
        training = TrainingRepository.get_by_slug(slug)
        if not training:
            raise NotFoundError('TRAINING_NOT_FOUND', 'Тренировка не найдена')
        lang = get_request_language(request)
        progress = TrainingRepository.get_progress(request.user, training)
        return Response(TrainingDetailSerializer(training, context={'progress': progress, 'language': lang}).data)


class TrainingStartView(APIView):
    def post(self, request, slug):
        training = TrainingRepository.get_by_slug(slug)
        if not training:
            raise NotFoundError('TRAINING_NOT_FOUND', 'Тренировка не найдена')
        progress, _ = TrainingRepository.start_or_get(request.user, training)
        return Response({'status': progress.status})


class TrainingCompleteView(APIView):
    def post(self, request, slug):
        training = TrainingRepository.get_by_slug(slug)
        if not training:
            raise NotFoundError('TRAINING_NOT_FOUND', 'Тренировка не найдена')
        lang = get_request_language(request)
        serializer = CompleteTrainingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        progress = TrainingRepository.complete(
            request.user, training,
            reflection_note=serializer.validated_data.get('reflection_note')
        )
        AcademyService.check_and_award_achievements(request.user)
        return Response(TrainingDetailSerializer(training, context={'progress': progress, 'language': lang}).data)


# ── Programs ──────────────────────────────────────────────────────────────────

class ProgramListView(APIView):
    def get(self, request):
        programs = ProgramRepository.list_all()
        lang = get_request_language(request)
        enrollments = {
            str(e.program_id): e
            for e in request.user.program_enrollments.select_related('program').all()
        }
        serializer = ProgramListSerializer(
            programs, many=True, context={'enrollments': enrollments, 'language': lang}
        )
        return Response({'count': len(serializer.data), 'results': serializer.data})


class ProgramDetailView(APIView):
    def get(self, request, slug):
        program = ProgramRepository.get_by_slug(slug)
        if not program:
            raise NotFoundError('PROGRAM_NOT_FOUND', 'Программа не найдена')
        lang = get_request_language(request)
        enrollment = ProgramRepository.get_enrollment(request.user, program)
        completed_days = (
            ProgramRepository.get_completed_day_numbers(enrollment) if enrollment else set()
        )
        return Response(ProgramDetailSerializer(
            program,
            context={'enrollment': enrollment, 'completed_days': completed_days, 'language': lang}
        ).data)


class ProgramEnrollView(APIView):
    def post(self, request, slug):
        program = ProgramRepository.get_by_slug(slug)
        if not program:
            raise NotFoundError('PROGRAM_NOT_FOUND', 'Программа не найдена')
        lang = get_request_language(request)
        enrollment, created = ProgramRepository.enroll(request.user, program)
        if not created and enrollment.status != 'paused':
            raise ConflictError('ALREADY_ENROLLED', 'Вы уже записаны на эту программу')
        if not created:
            enrollment.status = 'active'
            enrollment.save(update_fields=['status', 'updated_at'])
        completed_days = ProgramRepository.get_completed_day_numbers(enrollment)
        return Response(ProgramDetailSerializer(
            program,
            context={'enrollment': enrollment, 'completed_days': completed_days, 'language': lang}
        ).data, status=status.HTTP_201_CREATED)


class ProgramDayCompleteView(APIView):
    def post(self, request, slug, day_number):
        program = ProgramRepository.get_by_slug(slug)
        if not program:
            raise NotFoundError('PROGRAM_NOT_FOUND', 'Программа не найдена')
        lang = get_request_language(request)
        enrollment = ProgramRepository.get_enrollment(request.user, program)
        if not enrollment:
            raise NotFoundError('NOT_ENROLLED', 'Вы не записаны на эту программу')
        day = program.days.filter(day_number=day_number).first()
        if not day:
            raise NotFoundError('DAY_NOT_FOUND', f'День {day_number} не найден')
        serializer = CompleteDaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _, created = ProgramRepository.complete_day(
            enrollment, day, reflection=serializer.validated_data.get('reflection')
        )
        if created:
            AcademyService.check_and_award_achievements(request.user)
        completed_days = ProgramRepository.get_completed_day_numbers(enrollment)
        return Response(ProgramDetailSerializer(
            program,
            context={'enrollment': enrollment, 'completed_days': completed_days, 'language': lang}
        ).data)


# ── Micro practice ────────────────────────────────────────────────────────────

class MicroPracticeTodayView(APIView):
    def get(self, request):
        today = now().date()
        lang = get_request_language(request)
        practice, is_completed = MicroPracticeRepository.get_for_today(request.user, today)
        if not practice:
            return Response({'practice': None, 'is_completed': False})
        return Response({
            'practice': MicroPracticeSerializer(
                practice, context={'is_completed': is_completed, 'language': lang}
            ).data,
            'is_completed': is_completed,
        })


class MicroPracticeCompleteView(APIView):
    def post(self, request, practice_id):
        from .models import AcademyMicroPractice
        practice = AcademyMicroPractice.objects.filter(id=practice_id, is_active=True).first()
        if not practice:
            raise NotFoundError('PRACTICE_NOT_FOUND', 'Практика не найдена')
        today = now().date()
        created = MicroPracticeRepository.complete(request.user, practice, today)
        if created:
            AcademyService.check_and_award_achievements(request.user)
        return Response({'completed': True})


# ── Progress & recommendations ────────────────────────────────────────────────

class LearningProgressView(APIView):
    def get(self, request):
        data = AcademyService.get_learning_progress(request.user)
        return Response(LearningProgressSerializer(data).data)


class RecommendationsView(APIView):
    def get(self, request):
        from .serializers import ArticleListSerializer, TrainingListSerializer, ProgramListSerializer
        lang = get_request_language(request)
        recommendations = AcademyService.get_recommendations(request.user)
        result = []
        completed_ids = ArticleRepository.get_completed_ids_for_user(request.user)
        training_progress = TrainingRepository.get_all_progress_for_user(request.user)
        for rec in recommendations:
            item = rec['item']
            t = rec['type']
            if t == 'article':
                serialized = ArticleListSerializer(item, context={'completed_ids': completed_ids, 'language': lang}).data
            elif t == 'training':
                serialized = TrainingListSerializer(item, context={'training_progress': training_progress, 'language': lang}).data
            else:
                serialized = ProgramListSerializer(item, context={'enrollments': {}, 'language': lang}).data
            result.append({'type': t, 'reason': rec['reason'], 'item': serialized})
        return Response({'count': len(result), 'results': result})


class AchievementsView(APIView):
    def get(self, request):
        user_achievements = AchievementRepository.get_user_achievements(request.user)
        lang = get_request_language(request)
        serializer = UserAchievementSerializer(user_achievements, many=True, context={'language': lang})
        return Response({'count': len(serializer.data), 'results': serializer.data})


class ActiveProgramView(APIView):
    def get(self, request):
        enrollment = ProgramRepository.get_active_enrollment(request.user)
        if not enrollment:
            return Response({'active_program': None})
        lang = get_request_language(request)
        program = enrollment.program
        program.days.all()
        completed_days = ProgramRepository.get_completed_day_numbers(enrollment)
        return Response({
            'active_program': ProgramDetailSerializer(
                program,
                context={'enrollment': enrollment, 'completed_days': completed_days, 'language': lang}
            ).data
        })

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CoachRequestSerializer, MediatorRequestSerializer
from .services.coach_service import CoachService
from .services.mediator_service import MediatorService

logger = logging.getLogger(__name__)


class CoachView(APIView):
    """
    POST /api/v1/ai/coach/

    Тело запроса:
        {"message": "Мы часто ругаемся из-за денег", "conversation_id": "<uuid>" (опционально)}

    Ответ:
        {"response": "...", "conversation_id": "..."}

    Перед отправкой в OpenAI автоматически подгружает:
      - relationship_index (overall_score, crisis_level)
      - текущий уровень семьи (FamilyJourney.last_completed_level)
      - зональные показатели: communication, trust, intimacy, conflict, values, future
      - сильные стороны пары и корневую проблему
      - семейную конституцию (ценности, правила общения)
    """

    def post(self, request):
        serializer = CoachRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message         = serializer.validated_data['message']
        conversation_id = serializer.validated_data.get('conversation_id')

        try:
            service = CoachService()
            result  = service.chat(
                user=request.user,
                message=message,
                conversation_id=str(conversation_id) if conversation_id else None,
            )
            return Response(result, status=status.HTTP_200_OK)

        except ValueError as e:
            logger.warning('CoachView validation error for user %s: %s', request.user.id, e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except RuntimeError as e:
            logger.error('CoachView runtime error for user %s: %s', request.user.id, e)
            return Response(
                {'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except Exception as e:
            logger.error(
                'CoachView unexpected error for user %s: %s',
                request.user.id, e, exc_info=True,
            )
            return Response(
                {'error': 'Временная ошибка AI-сервиса. Попробуйте позже.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class MediatorView(APIView):
    """
    POST /api/v1/ai/mediator/

    Тело запроса:
        {"message": "Описание конфликта..."}

    Ответ:
        {"response": "...", "conversation_id": "..."}
    """

    def post(self, request):
        serializer = MediatorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message         = serializer.validated_data['message']
        conversation_id = serializer.validated_data.get('conversation_id')

        try:
            service = MediatorService()
            result  = service.analyze(
                user=request.user,
                description=message,
                conversation_id=str(conversation_id) if conversation_id else None,
            )
            return Response(result, status=status.HTTP_200_OK)

        except (ValueError, RuntimeError) as e:
            logger.warning('MediatorView error for user %s: %s', request.user.id, e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(
                'MediatorView unexpected error for user %s: %s',
                request.user.id, e, exc_info=True,
            )
            return Response(
                {'error': 'Временная ошибка AI-сервиса. Попробуйте позже.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

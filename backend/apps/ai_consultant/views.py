import json
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from shared.exceptions import NotFoundError, BusinessLogicError
from apps.couples.repositories import CoupleRepository
from .models import AIConversation
from .repositories import AIConversationRepository, AIMessageRepository
from .serializers import (
    ConversationSerializer, MessageSerializer,
    CreateConversationSerializer, SendMessageSerializer,
)
from .services import AIConsultantService


class ConversationListCreateView(APIView):
    def get(self, request):
        conversations = AIConversationRepository.list_for_user(request.user)
        data = ConversationSerializer(conversations, many=True).data
        return Response({'count': len(data), 'results': data})

    def post(self, request):
        couple = CoupleRepository.get_active_for_user(request.user)
        if not couple:
            raise BusinessLogicError('NO_COUPLE', 'Нет активной пары')
        serializer = CreateConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AIConsultantService.create_conversation(
            user=request.user,
            couple=couple,
            topic=serializer.validated_data.get('initial_topic'),
        )
        return Response(
            {
                'id': str(result['conversation'].id),
                'created_at': result['conversation'].created_at,
                'context_loaded': True,
                'greeting': result['greeting'],
            },
            status=status.HTTP_201_CREATED,
        )


class MessageListView(APIView):
    def get(self, request, conv_id):
        conversation = get_object_or_404(AIConversation, id=conv_id, user=request.user)
        before_id = request.query_params.get('before')
        limit = int(request.query_params.get('limit', 20))
        messages, has_more = AIMessageRepository.list_for_conversation(
            conversation, limit=limit, before_id=before_id
        )
        data = MessageSerializer(messages, many=True).data
        return Response({'count': len(data), 'results': data, 'has_more': has_more})


class MessageStreamView(APIView):
    def post(self, request, conv_id):
        conversation = get_object_or_404(AIConversation, id=conv_id, user=request.user)
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_message = serializer.validated_data['content']

        def event_stream():
            try:
                for chunk in AIConsultantService.stream_response(conversation, user_message):
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk}, ensure_ascii=False)}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream; charset=utf-8')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

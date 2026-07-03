from rest_framework import serializers
from .models import CoachConversation, CoachMessage


class CoachRequestSerializer(serializers.Serializer):
    message         = serializers.CharField(max_length=2000, trim_whitespace=True)
    conversation_id = serializers.UUIDField(required=False, allow_null=True, default=None)

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError('Сообщение не может быть пустым.')
        return value


class CoachResponseSerializer(serializers.Serializer):
    response        = serializers.CharField()
    conversation_id = serializers.UUIDField()


class MediatorRequestSerializer(serializers.Serializer):
    message         = serializers.CharField(max_length=2000, trim_whitespace=True)
    conversation_id = serializers.UUIDField(required=False, allow_null=True, default=None)


class CoachMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CoachMessage
        fields = ['id', 'role', 'content', 'created_at']


class CoachConversationSerializer(serializers.ModelSerializer):
    messages = CoachMessageSerializer(many=True, read_only=True)

    class Meta:
        model  = CoachConversation
        fields = ['id', 'dialog_type', 'title', 'created_at', 'messages']

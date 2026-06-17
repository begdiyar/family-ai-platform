from rest_framework import serializers
from .models import AIConversation, AIMessage


class ConversationSerializer(serializers.ModelSerializer):
    messages_count = serializers.SerializerMethodField()

    def get_messages_count(self, obj):
        return obj.messages.exclude(role=AIMessage.ROLE_SYSTEM).count()

    class Meta:
        model = AIConversation
        fields = ['id', 'title', 'messages_count', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMessage
        fields = ['id', 'role', 'content', 'created_at']


class CreateConversationSerializer(serializers.Serializer):
    initial_topic = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class SendMessageSerializer(serializers.Serializer):
    content = serializers.CharField(min_length=1, max_length=2000)

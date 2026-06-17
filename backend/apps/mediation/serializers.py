from rest_framework import serializers
from .models import ConflictSession, ConflictEntry


class ConflictEntrySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = ConflictEntry
        fields = ['id', 'user_name', 'description', 'feelings', 'desired_outcome', 'created_at']


class ConflictSessionSerializer(serializers.ModelSerializer):
    my_entry_submitted = serializers.SerializerMethodField()
    partner_entry_submitted = serializers.SerializerMethodField()

    def get_my_entry_submitted(self, obj):
        user = self.context.get('user')
        return user is not None and obj.get_entry(user) is not None

    def get_partner_entry_submitted(self, obj):
        user = self.context.get('user')
        couple = obj.couple
        partner = couple.get_partner(user) if user else None
        return partner is not None and obj.get_entry(partner) is not None

    class Meta:
        model = ConflictSession
        fields = ['id', 'title', 'status', 'my_entry_submitted',
                  'partner_entry_submitted', 'created_at']


class ConflictSessionDetailSerializer(ConflictSessionSerializer):
    ai_analysis = serializers.JSONField()

    class Meta(ConflictSessionSerializer.Meta):
        fields = ConflictSessionSerializer.Meta.fields + ['ai_analysis']


class SubmitEntrySerializer(serializers.Serializer):
    description = serializers.CharField(min_length=10)
    feelings = serializers.CharField(required=False, allow_blank=True, default='')
    desired_outcome = serializers.CharField(required=False, allow_blank=True, default='')

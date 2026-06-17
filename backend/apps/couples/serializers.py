from rest_framework import serializers
from .models import Couple, CoupleInvite
from .services import InviteService


class PartnerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    avatar_url = serializers.URLField(allow_null=True)


class InviteSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    def get_link(self, obj):
        return InviteService.build_invite_url(obj.token)

    class Meta:
        model = CoupleInvite
        fields = ['token', 'link', 'expires_at', 'status']


class CoupleShortSerializer(serializers.ModelSerializer):
    partner = serializers.SerializerMethodField()

    def get_partner(self, obj):
        request_user = self.context.get('request').user if self.context.get('request') else None
        if not request_user:
            return None
        partner = obj.get_partner(request_user)
        if not partner:
            return None
        return PartnerSerializer(partner).data

    class Meta:
        model = Couple
        fields = ['id', 'status', 'partner']


class CoupleDetailSerializer(serializers.ModelSerializer):
    partner_a = PartnerSerializer()
    partner_b = PartnerSerializer(allow_null=True)
    diagnostics_status = serializers.SerializerMethodField()
    invite = serializers.SerializerMethodField()

    def get_diagnostics_status(self, obj):
        from apps.diagnostics.repositories import DiagnosticRepository
        return DiagnosticRepository.get_couple_completion_status(obj)

    def get_invite(self, obj):
        from apps.couples.repositories import InviteRepository
        invite = InviteRepository.get_active_for_couple(obj)
        if invite:
            return InviteSerializer(invite).data
        return None

    class Meta:
        model = Couple
        fields = ['id', 'status', 'partner_a', 'partner_b', 'diagnostics_status', 'invite',
                  'has_children', 'children_count', 'marriage_year', 'created_at']


class AcceptInviteSerializer(serializers.Serializer):
    token = serializers.CharField()

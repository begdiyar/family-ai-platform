from rest_framework import serializers
from .models import Couple, CoupleInvite, Child, FamilyValue
from .services import InviteService


class PartnerSerializer(serializers.Serializer):
    id         = serializers.UUIDField()
    first_name = serializers.CharField()
    avatar_url = serializers.URLField(allow_null=True)


class InviteSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    def get_link(self, obj):
        return InviteService.build_invite_url(obj.token)

    class Meta:
        model  = CoupleInvite
        fields = ['token', 'link', 'expires_at', 'status']


class FamilyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FamilyValue
        fields = ['slug', 'label_ru']


class ChildSerializer(serializers.ModelSerializer):
    gender_label = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model  = Child
        fields = ['id', 'birth_date', 'gender', 'gender_label', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Child
        fields = ['birth_date', 'gender']

    def validate_gender(self, value):
        allowed = {'male', 'female', ''}
        if value not in allowed:
            raise serializers.ValidationError('Недопустимое значение пола.')
        return value


class FamilyContextSerializer(serializers.ModelSerializer):
    family_values = serializers.SlugRelatedField(
        many=True, slug_field='slug',
        queryset=FamilyValue.objects.all(),
    )

    class Meta:
        model  = Couple
        fields = [
            'relationship_status',
            'relationship_start_date',
            'marriage_date',
            'lives_with_parents',
            'relatives_influence_level',
            'religious_traditions_importance',
            'family_values',
        ]

    def validate_relatives_influence_level(self, value):
        if value is not None and not (1 <= value <= 5):
            raise serializers.ValidationError('Значение должно быть от 1 до 5.')
        return value

    def validate_religious_traditions_importance(self, value):
        if value is not None and not (1 <= value <= 5):
            raise serializers.ValidationError('Значение должно быть от 1 до 5.')
        return value


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
        model  = Couple
        fields = ['id', 'status', 'partner']


class CoupleDetailSerializer(serializers.ModelSerializer):
    partner_a           = PartnerSerializer()
    partner_b           = PartnerSerializer(allow_null=True)
    diagnostics_status  = serializers.SerializerMethodField()
    invite              = serializers.SerializerMethodField()
    family_values       = FamilyValueSerializer(many=True, read_only=True)
    children            = ChildSerializer(many=True, read_only=True)
    relationship_status_label = serializers.CharField(
        source='get_relationship_status_display', read_only=True,
    )

    def get_diagnostics_status(self, obj):
        from apps.diagnostics.repositories import DiagnosticRepository, JourneyRepository
        journey = JourneyRepository.get_for_couple(obj)
        level = journey.max_unlocked_level if journey else 1
        return DiagnosticRepository.get_couple_completion_status(obj, level)

    def get_invite(self, obj):
        from apps.couples.repositories import InviteRepository
        invite = InviteRepository.get_active_for_couple(obj)
        if invite:
            return InviteSerializer(invite).data
        return None

    class Meta:
        model  = Couple
        fields = [
            'id', 'status',
            'partner_a', 'partner_b',
            'diagnostics_status', 'invite',
            # relationship
            'relationship_status', 'relationship_status_label',
            'relationship_start_date', 'marriage_date',
            # legacy
            'has_children', 'children_count', 'marriage_year',
            # family context
            'lives_with_parents',
            'relatives_influence_level',
            'religious_traditions_importance',
            # related
            'family_values', 'children',
            'created_at',
        ]


class AcceptInviteSerializer(serializers.Serializer):
    token = serializers.CharField()


class FamilyValuesUpdateSerializer(serializers.Serializer):
    slugs = serializers.ListField(
        child=serializers.SlugField(),
        allow_empty=True,
    )

    def validate_slugs(self, value):
        existing = set(FamilyValue.objects.filter(slug__in=value).values_list('slug', flat=True))
        unknown = set(value) - existing
        if unknown:
            raise serializers.ValidationError(f'Неизвестные значения: {", ".join(sorted(unknown))}')
        return value

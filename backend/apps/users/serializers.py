from rest_framework import serializers
from .models import User, CommunicationPreference


class RegisterSerializer(serializers.Serializer):
    phone      = serializers.CharField(max_length=20)
    password   = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=100)

    def validate_phone(self, value):
        import re
        digits = re.sub(r'[\s\-\(\)\+]', '', value)
        if re.match(r'^998\d{9}$', digits):       # 998901111111
            return '+' + digits
        if re.match(r'^\d{9}$', digits):          # 901111111
            return '+998' + digits
        if re.match(r'^\+998\d{9}$', value.strip()):
            return value.strip()
        raise serializers.ValidationError('Введите номер в формате 901111111 или +998901111111')


def _normalize_phone(value: str) -> str:
    """Normalize UZ phone to +998XXXXXXXXX, return value as-is if not a phone."""
    import re
    digits = re.sub(r'[\s\-\(\)\+]', '', value)
    if re.match(r'^998\d{9}$', digits):
        return '+' + digits
    if re.match(r'^\d{9}$', digits):
        return '+998' + digits
    if re.match(r'^\+998\d{9}$', value.strip()):
        return value.strip()
    return value  # name or username — pass through


class LoginSerializer(serializers.Serializer):
    phone    = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    def validate_phone(self, value):
        return _normalize_phone(value.strip())


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid      = serializers.CharField()
    token    = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CommunicationPreferenceSerializer(serializers.ModelSerializer):
    conflict_style_label = serializers.CharField(source='get_conflict_style_display', read_only=True)
    support_style_label  = serializers.CharField(source='get_support_style_display',  read_only=True)

    class Meta:
        model  = CommunicationPreference
        fields = [
            'conflict_style', 'conflict_style_label',
            'support_style',  'support_style_label',
            'updated_at',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    couple               = serializers.SerializerMethodField()
    gender_label         = serializers.CharField(source='get_gender_display',          read_only=True)
    education_level_label = serializers.CharField(source='get_education_level_display', read_only=True)
    communication_pref   = serializers.SerializerMethodField()

    def get_couple(self, obj):
        couple = obj.get_active_couple()
        if not couple:
            return None
        from apps.couples.serializers import CoupleShortSerializer
        return CoupleShortSerializer(couple, context=self.context).data

    def get_communication_pref(self, obj):
        pref = getattr(obj, 'communication_pref', None)
        if pref is None:
            return None
        return CommunicationPreferenceSerializer(pref).data

    class Meta:
        model  = User
        fields = [
            'id', 'phone', 'email',
            'first_name', 'last_name',
            'birth_date',
            'gender', 'gender_label',
            'native_language',
            'occupation',
            'education_level', 'education_level_label',
            'avatar_url', 'preferred_language',
            'is_verified', 'is_staff', 'is_superuser',
            'couple',
            'communication_pref',
            'created_at',
        ]
        read_only_fields = ['id', 'phone', 'email', 'is_verified', 'is_staff', 'is_superuser', 'created_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = [
            'first_name', 'last_name', 'birth_date',
            'gender', 'native_language', 'occupation', 'education_level',
            'avatar_url', 'preferred_language',
        ]


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password     = serializers.CharField(min_length=8, write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Неверный текущий пароль')
        return value

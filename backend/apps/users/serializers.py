from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=100)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    couple = serializers.SerializerMethodField()

    def get_couple(self, obj):
        couple = obj.get_active_couple()
        if not couple:
            return None
        from apps.couples.serializers import CoupleShortSerializer
        return CoupleShortSerializer(couple, context=self.context).data

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'avatar_url', 'is_verified', 'couple', 'preferred_language', 'created_at']
        read_only_fields = ['id', 'email', 'is_verified', 'created_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'avatar_url', 'preferred_language']

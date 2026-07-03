from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import CommunicationPreference
from .serializers import (
    RegisterSerializer, LoginSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    LogoutSerializer, UserProfileSerializer, UserUpdateSerializer,
    CommunicationPreferenceSerializer, ChangePasswordSerializer,
)
from .services import AuthService, TokenService
from .repositories import UserRepository


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AuthService.register(**serializer.validated_data)
        return Response(
            {
                'user': UserProfileSerializer(result['user']).data,
                'tokens': result['tokens'],
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AuthService.login(**serializer.validated_data)
        return Response({
            'user': UserProfileSerializer(result['user']).data,
            'tokens': result['tokens'],
        })


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthService.logout(serializer.validated_data['refresh'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthService.request_password_reset(serializer.validated_data['email'])
        return Response({'message': 'Если email существует, письмо отправлено'})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthService.confirm_password_reset(
            uid_b64=serializer.validated_data['uid'],
            token=serializer.validated_data['token'],
            new_password=serializer.validated_data['password'],
        )
        return Response({'message': 'Пароль успешно изменён'})


class MeView(APIView):
    def get(self, request):
        return Response(UserProfileSerializer(request.user, context={'request': request}).data)

    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = UserRepository.update(request.user, **serializer.validated_data)
        return Response(UserProfileSerializer(user, context={'request': request}).data)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])
        return Response({'message': 'Пароль успешно изменён'})


class CommunicationPreferenceView(APIView):
    def get(self, request):
        pref, _ = CommunicationPreference.objects.get_or_create(user=request.user)
        return Response(CommunicationPreferenceSerializer(pref).data)

    def patch(self, request):
        pref, _ = CommunicationPreference.objects.get_or_create(user=request.user)
        serializer = CommunicationPreferenceSerializer(pref, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CommunicationPreferenceSerializer(pref).data)

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from shared.exceptions import BusinessLogicError, NotFoundError
from .models import User
from .repositories import UserRepository


class TokenService:
    @staticmethod
    def generate_for_user(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    @staticmethod
    def blacklist(refresh_token: str) -> None:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass


class AuthService:
    @staticmethod
    def register(email: str, password: str, first_name: str) -> dict:
        if UserRepository.email_exists(email):
            raise BusinessLogicError('EMAIL_ALREADY_EXISTS', 'Этот email уже зарегистрирован')
        user = UserRepository.create(email=email, password=password, first_name=first_name)
        tokens = TokenService.generate_for_user(user)
        EmailService.send_verification(user)
        return {'user': user, 'tokens': tokens}

    @staticmethod
    def login(email: str, password: str) -> dict:
        user = UserRepository.get_by_email(email)
        if not user or not user.check_password(password):
            raise BusinessLogicError('INVALID_CREDENTIALS', 'Неверный email или пароль')
        tokens = TokenService.generate_for_user(user)
        return {'user': user, 'tokens': tokens}

    @staticmethod
    def logout(refresh_token: str) -> None:
        TokenService.blacklist(refresh_token)

    @staticmethod
    def request_password_reset(email: str) -> None:
        user = UserRepository.get_by_email(email)
        if user:
            EmailService.send_password_reset(user)

    @staticmethod
    def confirm_password_reset(uid_b64: str, token: str, new_password: str) -> None:
        try:
            uid = force_str(urlsafe_base64_decode(uid_b64))
            user = UserRepository.get_by_id(uid)
        except Exception:
            user = None

        if not user or not default_token_generator.check_token(user, token):
            raise BusinessLogicError('TOKEN_INVALID_OR_EXPIRED', 'Ссылка недействительна или истекла')

        UserRepository.set_password(user, new_password)


class EmailService:
    @staticmethod
    def send_verification(user: User) -> None:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        link = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"
        send_mail(
            subject='Подтвердите email',
            message=f'Перейдите по ссылке для подтверждения: {link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

    @staticmethod
    def send_password_reset(user: User) -> None:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        send_mail(
            subject='Сброс пароля',
            message=f'Для сброса пароля перейдите по ссылке: {link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

import logging
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from shared.exceptions import BusinessLogicError, NotFoundError
from .models import User
from .repositories import UserRepository

logger = logging.getLogger(__name__)


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
            logger.warning("Failed to blacklist refresh token", exc_info=True)


class AuthService:
    @staticmethod
    def register(phone: str, password: str, first_name: str) -> dict:
        if UserRepository.phone_exists(phone):
            raise BusinessLogicError('PHONE_ALREADY_EXISTS', 'Этот номер телефона уже зарегистрирован')
        user = UserRepository.create(phone=phone, password=password, first_name=first_name)
        tokens = TokenService.generate_for_user(user)
        return {'user': user, 'tokens': tokens}

    @staticmethod
    def login(phone: str, password: str) -> dict:
        # Accept phone number, username (e.g. "admin") or first_name (case-insensitive)
        user = (
            UserRepository.get_by_phone(phone)
            or UserRepository.get_by_username(phone)
            or UserRepository.get_by_first_name(phone)
        )
        if not user:
            # Check if name exists but is ambiguous (multiple matches)
            from .models import User as UserModel
            if UserModel.objects.filter(first_name__iexact=phone, is_active=True).count() > 1:
                raise BusinessLogicError(
                    'AMBIGUOUS_NAME',
                    'Несколько аккаунтов с таким именем. Войдите по номеру телефона.'
                )
            raise BusinessLogicError('INVALID_CREDENTIALS', 'Неверные данные для входа')
        if not user.check_password(password):
            raise BusinessLogicError('INVALID_CREDENTIALS', 'Неверные данные для входа')
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

from typing import Optional
from .models import User


class UserRepository:
    @staticmethod
    def email_exists(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.objects.filter(email=email, is_active=True).first()

    @staticmethod
    def get_by_id(user_id) -> Optional[User]:
        return User.objects.filter(id=user_id, is_active=True).first()

    @staticmethod
    def create(email: str, password: str, first_name: str) -> User:
        return User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
        )

    @staticmethod
    def update(user: User, **fields) -> User:
        for key, value in fields.items():
            setattr(user, key, value)
        user.save(update_fields=list(fields.keys()) + ['updated_at'])
        return user

    @staticmethod
    def set_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        user.save(update_fields=['password', 'updated_at'])

    @staticmethod
    def mark_verified(user: User) -> None:
        user.is_verified = True
        user.save(update_fields=['is_verified', 'updated_at'])

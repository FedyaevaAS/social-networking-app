from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db.db import get_async_session
from app.core.db.models import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Получает базу данных пользователей.

    - **session**: Асинхронная сессия для работы с базой данных.

    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Возвращает стратегию JWT."""
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер пользователей для операций CRUD."""

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """
        Валидирует пароль пользователя.

        - **password**: Пароль для валидации.
        - **user**: Объект пользователя.

        """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason="Пароль должен содержать больше 3 символов."
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Пароль не должен содержать e-mail.")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """
        Вызывается после успешной регистрации пользователя.

        - **user**: Зарегистрированный пользователь.
        - **request**: Запрос, если есть (опционально).

        """
        print(f"Пользователь {user.email} зарегистрирован.")


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Получает менеджер пользователей.

    - **user_db**: База данных пользователей.

    """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud.post import post_crud
from app.core.db.models import Like


async def check_post_exists(
    post_id: int,
    session: AsyncSession,
) -> None:
    """
    Проверяет существование поста.

    - **post_id**: Идентификатор поста для проверки.
    - **session**: Асинхронная сессия для работы с базой данных.

    """
    post = await post_crud.get(post_id, session)
    if post is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Пост не найден!")
    return post


async def check_post_with_likes_exists(
    post_id: int,
    session: AsyncSession,
) -> None:
    """
    Проверяет существование поста с лайками.

    - **post_id**: Идентификатор поста для проверки.
    - **session**: Асинхронная сессия для работы с базой данных.

    """
    post = await post_crud.get_post_with_likes_by_id(post_id, session)
    if post is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Пост не найден!")
    return post


async def check_post_with_author_and_likes_exists(
    post_id: int,
    session: AsyncSession,
) -> None:
    """
    Проверяет существование поста с автором и лайками.

    - **post_id**: Идентификатор поста для проверки.
    - **session**: Асинхронная сессия для работы с базой данных.

    """
    post = await post_crud.get_post_with_author_and_likes_by_id(post_id, session)
    if post is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Пост не найден!")
    return post


async def check_text_duplicate(
    text: str,
    session: AsyncSession,
) -> None:
    """
    Проверяет наличие дубликата текста поста.

    - **text**: Текст поста для проверки.
    - **session**: Асинхронная сессия для работы с базой данных.

    """
    post = await post_crud.get_post_by_text(text, session)
    if post is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Такой пост уже существует!",
        )


async def check_post_author(
    author_id: int,
    user_id: int,
) -> None:
    """
    Проверяет авторство поста.

    - **author_id**: Идентификатор автора поста.
    - **user_id**: Идентификатор текущего пользователя.

    """
    if author_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="У вас недостаточно прав для выполнения этой операции.",
        )


async def check_post_author_for_like(
    author_id: int,
    user_id: int,
) -> None:
    """
    Проверяет авторство поста для лайка.

    - **author_id**: Идентификатор автора поста.
    - **user_id**: Идентификатор текущего пользователя.

    """
    if author_id == user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Вы не можете поставить лайк на свой пост.",
        )


async def checking_like_exists_to_leave(
    user_like: Optional[Like | None],
) -> None:
    """
    Проверяет ставил ли пользователь лайк на пост.

    - **user_like**: Лайк пользователя.

    """
    if user_like is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Вы уже ставили лайк на этот пост.",
        )


async def checking_like_exists_to_delete(
    user_like: Optional[Like | None],
) -> None:
    """
    Проверяет наличие лайка для удаления.

    - **user_like**: Лайк пользователя.

    """
    if user_like is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Вы не ставили лайк на этот пост.",
        )

from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators
from app.core.crud.like import like_crud
from app.core.crud.user import user_crud
from app.core.db.db import get_async_session
from app.core.db.models import User
from app.core.error import generate_error_responses
from app.core.user import current_user
from app.schemas.like import LikeDB, LikeDetailDB

router = APIRouter()


@router.get(
    "/{post_id}",
    response_model=list[LikeDetailDB],
    status_code=HTTPStatus.OK,
    responses=generate_error_responses(HTTPStatus.NOT_FOUND),
)
async def get_all_posts_likes(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить все лайки поста.

    - **post_id**: Идентификатор поста.
    - **session**: Асинхронная сессия для работы с базой данных.

    """
    post = await validators.check_post_with_likes_exists(post_id, session)
    for like in post.likes:
        user = await user_crud.get(like.author_id, session)
        setattr(like, "author", user)
    return post.likes


@router.post(
    "/{post_id}",
    response_model=LikeDB,
    status_code=HTTPStatus.CREATED,
    responses=generate_error_responses(
        HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED
    ),
)
async def leave_like(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Оставить лайк на посте.

    - **post_id**: Идентификатор поста.
    - **session**: Асинхронная сессия для работы с базой данных.
    - **user**: Текущий пользователь.

    """
    post = await validators.check_post_with_likes_exists(post_id, session)
    await validators.check_post_author_for_like(post.author_id, user.id)
    user_like = next((like for like in post.likes if like.author_id == user.id), None)
    await validators.checking_like_exists_to_leave(user_like)
    new_like = await like_crud.leave_like(user, post, session)
    return new_like


@router.delete(
    "/{post_id}",
    response_model=LikeDB,
    status_code=HTTPStatus.OK,
    responses=generate_error_responses(
        HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED
    ),
)
async def delete_like(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Удалить лайк с поста.

    - **post_id**: Идентификатор поста.
    - **session**: Асинхронная сессия для работы с базой данных.
    - **user**: Текущий пользователь.

    """
    post = await validators.check_post_with_likes_exists(post_id, session)
    user_like = next((like for like in post.likes if like.author_id == user.id), None)
    await validators.checking_like_exists_to_delete(user_like)
    return await like_crud.delete(user_like, session)

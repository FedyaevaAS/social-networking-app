from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import validators
from app.core.crud.post import post_crud
from app.core.db.db import get_async_session
from app.core.db.models import User
from app.core.error import generate_error_responses
from app.core.user import current_user
from app.schemas.post import PostCreate, PostDB, PostDetailDB, PostUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=list[PostDetailDB],
    status_code=HTTPStatus.OK,
)
async def get_all_posts(
    limit: int = Query(default=10, gt=0),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить все посты.

    - **limit**: Ограничение количества постов в ответе (по умолчанию 10).
    - **offset**: Смещение начала списка постов (по умолчанию 0).
    - **session**: Асинхронная сессия для работы с базой данных.

    """
    posts = await post_crud.get_all_posts(limit, offset, session)
    for post in posts:
        setattr(post, "likes_count", len(post.likes))
    return posts


@router.get(
    "/{post_id}",
    response_model=PostDetailDB,
    status_code=HTTPStatus.OK,
    responses=generate_error_responses(HTTPStatus.NOT_FOUND),
)
async def get_post_by_id(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить пост по его идентификатору.

    - **post_id**: Идентификатор поста.
    - **session**: Асинхронная сессия для работы с базой данных.

    """
    post = await validators.check_post_with_author_and_likes_exists(post_id, session)
    setattr(post, "likes_count", len(post.likes))
    return post


@router.post(
    "/",
    response_model=PostDB,
    status_code=HTTPStatus.CREATED,
    responses=generate_error_responses(HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED),
)
async def create_new_post(
    post: PostCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Создать новый пост.

    - **post**: Данные для создания поста.
    - **session**: Асинхронная сессия для работы с базой данных.
    - **user**: Текущий пользователь.

    """
    await validators.check_text_duplicate(post.text, session)
    new_post = await post_crud.create(post, session, user)
    return new_post


@router.patch(
    "/{post_id}",
    response_model=PostDB,
    status_code=HTTPStatus.OK,
    responses=generate_error_responses(
        HTTPStatus.FORBIDDEN, HTTPStatus.NOT_FOUND, HTTPStatus.UNAUTHORIZED
    ),
)
async def partially_update_post(
    post_id: int,
    updated_data: PostUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Частично обновить пост.

    - **post_id**: Идентификатор поста для обновления.
    - **updated_data**: Обновленные данные поста.
    - **session**: Асинхронная сессия для работы с базой данных.
    - **user**: Текущий пользователь.

    """
    post = await validators.check_post_exists(post_id, session)
    await validators.check_post_author(user.id, post.author_id)
    await validators.check_text_duplicate(updated_data.text, session)
    updated_post = await post_crud.update(post, updated_data, session)
    return updated_post


@router.delete(
    "/{post_id}",
    response_model=PostDB,
    status_code=HTTPStatus.OK,
    responses=generate_error_responses(HTTPStatus.UNAUTHORIZED),
)
async def delete_post(
    post_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удалить пост.

    - **post_id**: Идентификатор поста для удаления.
    - **user**: Текущий пользователь.
    - **session**: Асинхронная сессия для работы с базой данных.

    """
    post = await validators.check_post_exists(post_id, session)
    await validators.check_post_author(user.id, post.author_id)
    return await post_crud.delete(post, session)

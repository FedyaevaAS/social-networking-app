from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.crud.base import CRUDBase
from app.core.db.models import Post


class CRUDPost(CRUDBase):
    """CRUD операции для модели Post."""

    async def get_post_with_author_and_likes_by_id(
        self, post_id: int, session: AsyncSession
    ):
        """
        Получает пост с автором и лайками по его идентификатору.

        - **post_id**: Идентификатор поста.
        - **session**: Асинхронная сессия для работы с базой данных.

        """
        post = await session.execute(
            select(Post)
            .where(Post.id == post_id)
            .options(selectinload(Post.author), selectinload(Post.likes))
        )
        post = post.scalars().first()
        return post

    async def get_post_by_text(self, text: str, session: AsyncSession):
        """
        Получает пост по его тексту.

        - **text**: Текст поста.
        - **session**: Асинхронная сессия для работы с базой данных.

        """
        post = await session.execute(select(Post).where(Post.text == text))
        post = post.scalars().first()
        return post

    async def get_post_with_likes_by_id(self, post_id: int, session: AsyncSession):
        """
        Получает пост с лайками по его идентификатору.

        - **post_id**: Идентификатор поста.
        - **session**: Асинхронная сессия для работы с базой данных.

        """
        post = await session.execute(
            select(Post).where(Post.id == post_id).options(selectinload(Post.likes))
        )
        post = post.scalars().first()
        return post

    async def get_all_posts(self, limit: int, offset: int, session: AsyncSession):
        """
        Получает все посты с авторами и лайками.

        - **limit**: Максимальное количество постов для получения.
        - **offset**: Смещение для получения постов.
        - **session**: Асинхронная сессия для работы с базой данных.

        """
        post = await session.execute(
            select(Post)
            .options(selectinload(Post.author), selectinload(Post.likes))
            .limit(limit)
            .offset(offset)
        )
        posts = post.scalars().all()
        return posts


post_crud = CRUDPost(Post)

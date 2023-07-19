from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud.base import CRUDBase
from app.core.db.models import Like, Post, User


class CRUDPost(CRUDBase):
    """CRUD операции для модели Post."""

    async def leave_like(self, author: User, post: Post, session: AsyncSession):
        """
        Оставить лайк на посте.

        - **author**: Пользователь, оставляющий лайк.
        - **post**: Пост, на который оставляется лайк.
        - **session**: Асинхронная сессия для работы с базой данных.

        """
        db_obj = Like(post=post, author=author)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


like_crud = CRUDPost(Like)

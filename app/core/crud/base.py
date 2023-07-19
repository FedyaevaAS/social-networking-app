from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models import User


class CRUDBase:
    def __init__(self, model):
        """
        Базовый класс для CRUD операций.

        - **model**: Модель базы данных.

        """
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """
        Получает объект из базы данных по его идентификатору.

        - **obj_id**: Идентификатор объекта.
        - **session**: Асинхронная сессия для работы с базой данных.

        """
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        """
        Создает новый объект в базе данных.

        - **obj_in**: Входные данные для создания объекта.
        - **session**: Асинхронная сессия для работы с базой данных.
        - **user**: Пользователь, связанный с объектом (опционально).

        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["author_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """
        Обновляет объект в базе данных.

        - **db_obj**: Обновляемый объект.
        - **obj_in**: Входные данные для обновления объекта.
        - **session**: Асинхронная сессия для работы с базой данных.

        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """
        Удаляет объект из базы данных.

        - **db_obj**: Удаляемый объект.
        - **session**: Асинхронная сессия для работы с базой данных.

        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

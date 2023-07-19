from datetime import date

from pydantic import BaseModel

from app.schemas.user import UserRead


class LikeDB(BaseModel):
    """Схема для отображения информации о лайке (Like)."""

    id: int
    created_at: date

    class Config:
        orm_mode = True


class LikeDetailDB(BaseModel):
    """Схема для отображения подробной информации о лайке (Like)."""

    id: int
    author: UserRead
    created_at: date

    class Config:
        orm_mode = True

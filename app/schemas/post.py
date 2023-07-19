from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserRead


class PostCreate(BaseModel):
    """Схема для создания поста (Post)."""

    text: str


class PostUpdate(BaseModel):
    """Схема для обновления поста (Post)."""

    text: Optional[str]


class PostDB(PostCreate):
    """Схема для отображения информации о посте (Post)."""

    id: int
    created_at: date

    class Config:
        orm_mode = True


class PostDetailDB(PostDB):
    """Схема для отображения подробной информации о посте (Post)."""

    author: UserRead
    likes_count: int

    class Config:
        orm_mode = True

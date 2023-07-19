from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Column, Integer, Text, func
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey


@as_declarative()
class Base:
    """Базовая модель."""

    id = Column(Integer, primary_key=True)
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
        onupdate=func.current_timestamp(),
    )


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель для пользователей."""

    __tablename__ = "users"

    posts = relationship("Post", back_populates="author")
    likes = relationship("Like", back_populates="author")


class Post(Base):
    """Модель для постов."""

    __tablename__ = "posts"

    text = Column(Text, unique=True, nullable=False)
    author_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")


class Like(Base):
    """Модель для лайков."""

    __tablename__ = "likes"

    author_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    author = relationship("User", back_populates="likes")
    post_id = Column(Integer, ForeignKey(Post.id), nullable=True)
    post = relationship("Post", back_populates="likes")

from app.core.crud.base import CRUDBase
from app.core.db.models import User


class CRUDPost(CRUDBase):
    """CRUD операции для модели User."""

    pass


user_crud = CRUDPost(User)

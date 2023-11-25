from src.models.users import Users
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = Users

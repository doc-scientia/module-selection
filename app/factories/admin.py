import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.schemas.admin import Admin


class AdminFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Admin
        sqlalchemy_session_persistence = "commit"

    username: str = factory.Faker("pystr_format", string_format="###???")

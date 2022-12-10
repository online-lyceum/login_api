from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from login_api.db.base import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    login = Column(String, unique=True)
    password = Column(String)


class TokenDB(Base):
    __tablename__ = "tokens"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_login = Column(String)
    key = Column(String)


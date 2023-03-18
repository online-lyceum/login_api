from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Time
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import Date
from db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True,
                       index=True)
    name = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

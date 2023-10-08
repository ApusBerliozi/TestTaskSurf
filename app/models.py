from sqlalchemy import Column, Integer, String, Uuid, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from datetime import datetime
import enum

Base = declarative_base()


class UserRoleEnum(enum.Enum):
    admin = "admin"
    customer = "customer"
    moderator = "moderator"


class AdvertisementEnum(enum.Enum):
    buy_order = "buy_order"
    sell_order = "sell_order"
    service = "service"


class ComplaintEnum(enum.Enum):
    adult_content = "adult_content"
    politic = "politic"
    insults = "insults"


class UserModel(Base):
    __tablename__ = "users"

    uuid = Column(Uuid, primary_key=True, index=True, server_default=text("gen_random_uuid()"))
    name = Column(String, unique=False)
    surname = Column(String, unique=False)
    login = Column(String, unique=True)
    password = Column(String, unique=True)
    role = Column(Enum(UserRoleEnum), index=True, default="customer")
    is_banned = Column(Boolean, unique=False, default=False, nullable=False)


class AdvertisementModel(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_uuid = Column(Uuid, ForeignKey("users.uuid"))
    caption = Column(String, unique=False)
    content = Column(String, unique=False)
    type = Column(Enum(AdvertisementEnum), nullable=True, default="service")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class ComplaintModel(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id"), nullable=False)
    content = Column(String, unique=False)
    type = Column(Enum(ComplaintEnum), nullable=True, default="insults")
    created_at = Column(DateTime, default=datetime.utcnow)
    user_uuid = Column(Uuid, ForeignKey("users.uuid"))


class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id"), nullable=False)
    user_uuid = Column(Uuid, ForeignKey("users.uuid"))
    content = Column(String, unique=False)
    created_at = Column(DateTime, default=datetime.utcnow)


from sqlalchemy import Column, Integer, String, Uuid, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from datetime import datetime


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    uuid = Column(Uuid, primary_key=True, index=True, server_default=text("uuid_generate_v4()"))
    name = Column(String, unique=False)
    surname = Column(String, unique=False)
    login = Column(String, unique=True)
    password = Column(String, unique=True)
    role = Column(Enum("admin", "customer", "moderator"), index=True, default="customer")
    is_banned = Column(Boolean, unique=False, default=False, nullable=False)

    advertisements = relationship("AdvertisementModel", back_populates="users")
    complaints = relationship("ComplaintModel", back_populates="users")
    comments = relationship("CommentModel", back_populates="users")


class AdvertisementModel(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True, server_default="nextval('advertisements_id_seq'::regclass)")
    user_uuid = Column(Uuid, ForeignKey("user.uuid"))
    caption = Column(String, unique=False)
    content = Column(String, unique=False)
    type = Column(Enum("покупка", "продажа", "услуга"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    complaints = relationship("Complaint", back_populates="advertisements")


class ComplaintModel(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True, server_default="nextval('complaints_id_seq'::regclass)")
    advertisement_id = Column(Integer, ForeignKey("advertisements.id"), nullable=False)
    content = Column(String, unique=False)
    type = Column(Enum("взрослый контент", "политика", "оскорбления"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_uuid = Column(Uuid, ForeignKey("user.uuid"))


class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, server_default="nextval('comments_id_seq'::regclass)")
    advertisement_id = Column(Integer, ForeignKey("advertisements.id"), nullable=False)
    user_uuid = Column(Uuid, ForeignKey("user.uuid"))
    content = Column(String, unique=False)
    created_at = Column(DateTime, default=datetime.utcnow)


from sqlalchemy import Column, Integer, String, Uuid, Enum, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

from server_params.db import db_engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    uuid = Column(Uuid, primary_key=True, index=True)
    name = Column(String, unique=False, index=True)
    surname = Column(String, unique=False)
    login = Column(String, unique=True)
    password = Column(String, unique=True)
    role = Column(Enum("admin", "customer", "moderator"), index=True, default="customer")

    advertisements = relationship("Advertisement", back_populates="users")


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(Uuid, ForeignKey("user.uuid"))
    name = Column(String, unique=False)
    content = Column(String, unique=False)
    type = Column(Enum("покупка", "продажа", "услуга"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    complaints = relationship("Complaint", back_populates="advertisements")


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id"), nullable=False)
    content = Column(String, unique=False)
    type = Column(Enum("взрослый контент", "политика", "оскорбления"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    advertisement_id = Column(Integer, ForeignKey("advertisements.id"), nullable=False)
    content = Column(String, unique=False)
    created_at = Column(DateTime, default=datetime.utcnow)


user_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
advertisement_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
complaint_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
comment_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)



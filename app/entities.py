import typing
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class User(BaseModel):
    uuid: str
    name: str
    surname: str


class Credentials(BaseModel):
    login: str
    password: str


class NewUser(Credentials):
    name: str
    surname: str


class AdvertisementType(Enum):
    buy_order = "buy_order"
    sell_order = "sell_order"
    service = "service"


class Comment(BaseModel):
    content: str
    published_at: datetime | None = None
    id: int | None = None
    user: User | None = None


class Advertisement(BaseModel):
    name: str
    type: AdvertisementType
    content: str
    user: User = None
    publication_time: datetime | None = None
    id: int | None = None


class NewAdvertisement(BaseModel):
    name: str
    type: AdvertisementType
    content: str


class TestResponse(BaseModel):
    content: str


class ComplaintType(Enum):
    adult_content = "adult_content"
    politic = "politic"
    insults = "insults"


class Complaint(BaseModel):
    content: str
    type: ComplaintType
    user: User | dict = None
    publication_time: datetime | None = None
    id: int | None = None


class NewComplaint(BaseModel):
    content: str
    type: ComplaintType


class NewComment(BaseModel):
    content: str


@dataclass
class AdvertisementFilter:
    type: AdvertisementType | None = None
    user_id: int | None = None


@dataclass
class CommentFilter:
    user_id: typing.Optional[int] = None


@dataclass
class ComplaintFilter:
    type: typing.Optional[ComplaintType] = None


@dataclass
class AdvertisementSort:
    publication_time: typing.Optional[str] = None


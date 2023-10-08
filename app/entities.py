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


class NewComment(BaseModel):
    content: str


class Comment(NewComment):
    published_at: datetime
    id: int
    user: User


class NewAdvertisement(BaseModel):
    name: str
    type: AdvertisementType
    content: str


class Advertisement(NewAdvertisement):
    user: User
    publication_time: datetime
    id: int


class TestResponse(BaseModel):
    content: str


class ComplaintType(Enum):
    adult_content = "adult_content"
    politic = "politic"
    insults = "insults"


class NewComplaint(BaseModel):
    content: str
    type: ComplaintType


class Complaint(NewComplaint):
    user: User
    publication_time: datetime
    id: int


@dataclass
class AdvertisementFilter:
    type: AdvertisementType | None = None


@dataclass
class CommentFilter:
    user_uuid: typing.Optional[str] = None


@dataclass
class ComplaintFilter:
    type: typing.Optional[ComplaintType] = None


@dataclass
class AdvertisementSort:
    publication_time: typing.Optional[bool] = False


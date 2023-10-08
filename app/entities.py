import typing
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class User(BaseModel):
    uuid: str
    name: str
    surname: str


class Credentials(BaseModel):
    nickname: str
    password: str


class AdvertisementType(Enum):
    buy_order = "покупка"
    sell_order = "продажа"
    service = "услуга"


class Comment(BaseModel):
    id: int
    user: User
    content: str


class Advertisement(BaseModel):
    id: str
    user: User
    name: str
    type: AdvertisementType
    comments: typing.List[Comment]
    content: str
    publication_time: str


class TestResponse(BaseModel):
    content: str


class ComplaintType(Enum):
    adult_content = "взрослый контент"
    politic = "политика"
    insults = "оскорбления"


class Complaint(BaseModel):
    id: int
    user: User
    content: str
    type: ComplaintType
    publication_time: str


@dataclass
class AdvertisementFilter:
    type: AdvertisementType | None = None
    user_id: int | None = None


@dataclass
class CommentFilter:
    user_id: typing.Optional[int] = None


@dataclass
class ComplaintFilter:
    user_id: typing.Optional[int] = None
    type: typing.Optional[ComplaintType] = None


@dataclass
class AdvertisementSort:
    publication_time: typing.Optional[str] = None


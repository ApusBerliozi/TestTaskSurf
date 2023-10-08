import typing
from dataclasses import dataclass
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
    buy_order = "покупка"
    sell_order = "продажа"
    service = "услуга"


class Comment(BaseModel):
    content: str
    id: int = None
    user: User = None


class Advertisement(BaseModel):
    name: str
    type: AdvertisementType
    content: str
    user: User = None
    publication_time: str = None
    id: str = None


class TestResponse(BaseModel):
    content: str


class ComplaintType(Enum):
    adult_content = "взрослый контент"
    politic = "политика"
    insults = "оскорбления"


class Complaint(BaseModel):
    content: str
    type: ComplaintType
    user: User = None
    publication_time: str = None
    id: int = None


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


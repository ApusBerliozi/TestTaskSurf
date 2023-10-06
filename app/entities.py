import typing
from enum import Enum

from pydantic import BaseModel


class User(BaseModel):
    uuid: int
    name: str
    surname: str


class Credentials(BaseModel):
    nickname: str
    password: str


class AdvertisementType(Enum):
    buy_order = "Покупка"
    sell_order = "Продажа"
    service = "Услуга"


class Comment(BaseModel):
    id_: int
    user: User
    content: str


class Complaint(BaseModel):
    id_: int
    user: User
    content: str


class Advertisement(BaseModel):
    id_: str
    user: User
    name: str
    type: AdvertisementType
    comments: typing.List[Comment]
    content: str
    complaints: typing.List[Complaint]


class TestResponse(BaseModel):
    content: str

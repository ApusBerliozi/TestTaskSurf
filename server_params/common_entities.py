import typing
from dataclasses import dataclass

from datetime import datetime
from pydantic import BaseModel, Field


class ServerResponse(BaseModel):
    description: str = "string"
    content: typing.Union[typing.Type[BaseModel], typing.List[typing.Type[BaseModel]], dict] = {}
    datetime: str = datetime.now().date()
    status: int = Field(200, description="The status code as an integer")


@dataclass
class Paginator:
    limit: int = 12
    page: int = 1


@dataclass
class Config:
    jwt_user_secret_key: str
    jwt_admin_secret_key: str


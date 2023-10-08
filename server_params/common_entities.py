import typing
from dataclasses import dataclass

from datetime import datetime
from pydantic import BaseModel, Field


@dataclass
class Paginator:
    limit: int = 12
    page: int = 1


class ServerResponse(BaseModel):
    description: str = "string"
    content: typing.Union[typing.Type[BaseModel], typing.List[typing.Any], dict] = {}
    datetime: str = str(datetime.now().date())
    status: int = Field(200, description="The status code as an integer")


@dataclass
class Config:
    jwt_user_secret_key: str
    jwt_admin_secret_key: str
    bot_token: str
    dev_chat_id: str

    db_username: str
    db_password: str
    db_host: str
    db_name: str


from fastapi import FastAPI, Depends
from app.entities import Credentials, Advertisement, Comment, Complaint, AdvertisementFilter, CommentFilter, \
    AdvertisementSort, ComplaintFilter
from app.query_parsers import parse_advertisements_filtr, parse_advertisement_sort_params, parse_comment_filtr, \
    parse_complaint_filtr
from libs.jwt_token import verify_user_token, verify_admin_token
from libs.response_generator import hint_factory
from server_params.common_entities import ServerResponse, Paginator
from server_params.paginator import get_paginator

app = FastAPI()


@app.post("/user/sign_up/")
async def sign_up(credentials: Credentials,) -> hint_factory({"jwt_token": str},
                                                             description="Зарегистрировался новый пользователь"):
    user_token = ...
    return ServerResponse(content={"jwt_token": user_token},
                          description="Зарегистрировался новый пользователь")


@app.get("/user/sign_in/")
async def sign_in(credentials: Credentials,) -> hint_factory({"jwt_token": str},
                                                             description="Пользователь вошёл в систему"):
    user_token = ...
    return ServerResponse(content={"jwt_token": user_token},
                          description="Пользователь вошёл в систему")


@app.get("/advertisements/")
async def get_advertisements(paginator: Paginator = Depends(get_paginator),
                             filtr: AdvertisementFilter = Depends(parse_advertisements_filtr),
                             sort_by: AdvertisementSort = Depends(parse_advertisement_sort_params),) -> hint_factory((Advertisement,),
                                                                                                                     description="Получен список объявлений"):
    advertisements = ...
    return ServerResponse(content=advertisements,
                          description="Получен список объявлений")


@app.post("/advertisements/")
async def create_advertisement(token: str = Depends(verify_user_token),) -> hint_factory(Advertisement,
                                                                                         description="Создано новое объявление"):
    advertisement = ...
    return ServerResponse(content=advertisement,
                          description="Создано новое объявление")


@app.get("/advertisements/{advertisement_id:int}/")
async def get_advertisement(advertisement_id: int,) -> hint_factory(Advertisement,
                                                                    description="Полученно объявление"):
    advertisement = ...
    return ServerResponse(content=advertisement,
                          description=f"Полученно объявление с id {advertisement_id}")


@app.delete("/advertisements/{advertisement_id:int}/")
async def remove_advertisement(advertisement_id: int,
                               token: str = Depends(verify_user_token),) -> hint_factory({"status": int},
                                                                                         description="Удаленно объявление"):
    ...
    return ServerResponse(description=f"Удаленно объявление с id {advertisement_id}")


@app.get("/advertisements/{advertisement_id:int}/comments/")
async def get_adv_comments(advertisement_id: int,
                           paginator: Paginator = Depends(get_paginator),
                           filtr: CommentFilter = Depends(parse_comment_filtr),) -> hint_factory((Comment,),
                                                                                    description="Полученны комментарии для объявления"):
    comments = ...
    return ServerResponse(content=comments,
                          description=f"Полученны комментарии для объявления с id {advertisement_id}")


@app.delete("/advertisements/{advertisement_id:int}/comments/{comment_id:int}/")
async def delete_comment(advertisement_id: int,
                         comment_id: int,
                         token: str = Depends(verify_admin_token),) -> hint_factory(Comment,
                                                                                    description="Удалён комментарий"):
    ...
    return ServerResponse(description=f"Удалён комментарий с id {comment_id} для объявления {advertisement_id}")


@app.post("/advertisements/{advertisement_id:int}/comments/")
async def create_comment(advertisement_id: int,
                         token: str = Depends(verify_user_token),) -> hint_factory(Comment,
                                                                                   description="Создан комментарий для объявления"):
    comment = ...
    return ServerResponse(content=comment,
                          description=f"Создан комментарий для объявления {advertisement_id}")


@app.post("/admins/")
async def create_admin(token: str = Depends(verify_admin_token),) -> hint_factory({"admin_token": str},
                                                                                  description="Создан новый администратор"):
    admin_token = ...
    return ServerResponse(content=admin_token,
                          description=f"Создан новый администратор")


@app.post("/advertisements/{advertisement_id:int}/complaints/")
async def create_complaint(advertisement_id: int,
                           token: str = Depends(verify_user_token),) -> hint_factory(Complaint,
                                                                                     description="Создана жалоба на объявление"):
    complaint = ...
    return ServerResponse(content=complaint,
                          description=f"Создана жалоба на объявление {advertisement_id}")


@app.get("/advertisements/{advertisement_id:int}/complaints/")
async def receive_complaints(advertisement_id: int,
                             paginator: Paginator = Depends(get_paginator),
                             filtr: ComplaintFilter = Depends(parse_complaint_filtr),
                             token: str = Depends(verify_admin_token),) -> hint_factory((Complaint,),
                                                                                        description="Получены жалобы на объявление"):
    complaints = ...
    return ServerResponse(content=complaints,
                          description=f"Получены жалобы на объявление {advertisement_id}")

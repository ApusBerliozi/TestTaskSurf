from fastapi import FastAPI, Depends
from app.entities import Credentials, Advertisement, Comment
from libs.response_generator import response_model_factory

app = FastAPI()


@app.post("/user/sign_up/")
async def sign_up(credentials: Credentials) -> response_model_factory({"jwt_token": str}):
    user_token = ...
    return {
        "content": {
            "jwt_token": user_token}
    }


@app.get("/user/sign_in/")
async def sign_in(credentials: Credentials, token: str = Depends(...)) -> response_model_factory({"jwt_token": str}):
    user_token = ...
    return {
        "status": 200,
        "content": {
            "jwt_token": user_token}
    }


@app.get("/advertisements/")
async def get_advertisements(limit: int) -> response_model_factory([Advertisement]):
    advertisements = ...
    return {"status": 200,
            "content": advertisements}


@app.post("/advertisements/")
async def create_advertisement(token: str = Depends(...)) -> response_model_factory(Advertisement):
    advertisement = ...
    return {
        "status": 200,
        "content": {
            "advertisement": advertisement}
    }


@app.get("/advertisements/{advertisement_id}/")
async def get_advertisement(advertisement_id: int) -> response_model_factory(Advertisement):
    advertisement = ...
    return {
        "status": 200,
        "content": {
            "advertisement": advertisement}
    }


@app.delete("/advertisements/{advertisement_id}/")
async def remove_advertisement(token: str = Depends(...)) -> response_model_factory({"status": int}):
    ...
    return {"status": 200}


@app.get("/advertisements/{advertisement_id}/comments/")
async def get_adv_comments() -> response_model_factory([Comment]):
    comments = ...
    return {
        "status": 200,
        "content": comments
    }


@app.delete("/advertisements/{advertisement_id}/comments/{comment_id}/")
async def delete_comment(token: str = Depends(...)) -> response_model_factory(Comment):
    ...
    return {"status": 200}


@app.post("/advertisements/{advertisement_id}/comments/")
async def create_comment(token: str = Depends(...)) -> response_model_factory(Comment):
    comment = ...
    return {
        "status": 200,
        "content": {
            "advertisement": comment}
    }


@app.post("/admins/")
async def create_admin(token: str = Depends(...)) -> response_model_factory({"jwt_token": str}):
    admin_token = ...
    return {
        "status": 200,
        "content": {
            "admin-token": admin_token}
    }


from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from config.config_reader import config


def create_user_token(user_uuid: str) -> str:
    payload = {
        "user_uuid": user_uuid,
    }

    jwt_token = jwt.encode(payload=payload, key=config.jwt_user_secret_key, algorithm='HS256')
    return jwt_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_user_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_admin_token(token=token)
    except:
        payload = False
    if payload:
        return payload
    try:
        payload = jwt.decode(jwt=token, key=config.jwt_user_secret_key, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_admin_token(user_uuid: str) -> str:
    payload = {
        "user_uuid": user_uuid
    }

    jwt_token = jwt.encode(payload=payload, key=config.jwt_admin_secret_key, algorithm='HS256')
    return jwt_token


def verify_admin_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(jwt=token, key=config.jwt_admin_secret_key, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import JWTDecodeError
from jwt.jwt import JWT
from app.entities import Credentials


def create_user_token(credentials: Credentials) -> str:
    payload = {
        "username": credentials.nickname,
        "password": credentials.password,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }

    jwt_token = JWT().encode(payload=payload, key=config.jwt_user_secret_key, alg='HS256')
    return jwt_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_user_token(token: str = Depends(oauth2_scheme)):
    try:
        # Verify and decode the token using the secret key
        payload = JWT().decode(message=token, key=config.jwt_user_secret_key, algorithms={"HS256"})
        return payload
    except JWTDecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_admin_token(credentials: Credentials) -> str:
    payload = {
        "username": credentials.nickname,
        "password": credentials.password
    }

    jwt_token = JWT().encode(payload=payload, key=config.jwt_admin_secret_key, alg='HS256')
    return jwt_token


def verify_admin_token(token: str = Depends(oauth2_scheme)):
    try:
        # Verify and decode the token using the secret key
        payload = JWT().decode(message=token, key=config.jwt_admin_secret_key, algorithms={"HS256"})
        return payload
    except JWTDecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

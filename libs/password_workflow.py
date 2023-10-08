from fastapi import HTTPException

from argon2 import PasswordHasher


ph = PasswordHasher()


def hash_password(password: str) -> str:
    hash_ = ph.hash(password=password)
    return hash_


def check_password(password: str,
                   hash: str):
    try:
        ph.verify(hash, password)
    except:
        raise HTTPException(status_code=400, detail="Password isn't correct")
    return True

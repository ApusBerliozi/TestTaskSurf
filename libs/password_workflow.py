import argon2


def hash_password(password: str):
    password = argon2.hash_password(password=password.encode())
    return password


def check_password(password: str,
                   hashed_password: str):
    if argon2.verify_password(password.encode(),
                              hashed_password.encode()):
        return True
        

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def has(password:str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify_password(plain_password,hashed_password)
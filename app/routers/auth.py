from passlib.context import CryptContext
from fastapi import Depends,HTTPException
from jose import JWTError, jwt
from datetime import datetime,timedelta
import os
from dotenv import load_dotenv
from app.database import SessionLocal
from fastapi.security import oauth2,OAuth2PasswordBearer
from .. import schemas

load_dotenv()




SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")





def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algoritm =[ALGORITHM])
    return encoded_jwt


def verify_access_token(token:str , credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY, algoriht=[ALGORITHM]) 
        id:str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data



def get_current_user(token : str = Depends (oauth2_schema)):
        credentials_exception = HTTPException(status_code= '401', headers={"WWW-Authenticate":"Bearer"})
        return verify_access_token(token, credentials_exception)

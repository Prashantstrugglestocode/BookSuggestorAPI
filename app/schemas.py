from pydantic import BaseModel,EmailStr
import sqlalchemy
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    email: EmailStr
    

    class Config:
        orm_mode = True

class Book(BaseModel):
    title: str
    author: str
    description: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True

class Book(BaseModel):
    title: str
    author: str
    description: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str  
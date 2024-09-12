from pydantic import BaseModel,EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    books: List[str]

    class Config:
        orm_mode = True

class Book(BaseModel):
    title: str
    author: str
    description: str

    class Config:
        orm_mode = True

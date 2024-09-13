import fastapi
import pydantic
from sqlalchemy.orm import Session
from app.oauth import SECRET_KEY
from . import models, schemas
from . import utils
from fastapi import Depends
from .database import get_db

def get_user_by_email(email: str, db:Session= Depends(get_db)):
    return db.query(models.User).filter(models.User.email == email).first();

def create_user(user:schemas.User, db:Session= Depends(get_db)):
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(email = user.email, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def add_book_to_user(user: models.User, book: schemas.Book, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    user.books.append(db_book)
    db.commit()
    return db_book
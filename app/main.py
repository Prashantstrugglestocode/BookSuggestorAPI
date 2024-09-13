from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, oauth
from .database import engine, get_db
from .oauth import create_access_token
from dotenv import load_dotenv
import os


API_KEY = os.getenv('API_KEY')

import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




# Register user
@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# User Login
@app.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not oauth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Search for books via Google Books API
@app.get("/search_books/")
def search_books(book_name: str, author_name: str):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={book_name}+inauthor:{author_name}s&key={API_KEY}")
    return response.json()

# Save a book to user's profile
@app.post("/users/{user_id}/books/")
def save_book(user_id: int, book: schemas.Book, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.add_book_to_user(db,user=db_user, book=book)
 
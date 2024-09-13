from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud, oauth
from .database import engine, get_db
from .oauth import create_access_token, get_current_user
from dotenv import load_dotenv
from . import utils
import os
import requests
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Outputs logs to the console
        # You can also add file handlers if needed
        # logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv('API_KEY')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register user-
@app.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = crud.get_user_by_email(email=user.email, db=db)
    if db_user:
        logger.warning(f"Registration attempt with already registered email: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the new user
    new_user = crud.create_user(user=user, db=db)
    
    logger.info(f"New user registered: {user.email}")
    return new_user

# User Login
@app.post("/login/")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {user_credentials.email}")
    
    db_user = crud.get_user_by_email(email=user_credentials.email, db=db)
    if not db_user:
        logger.warning(f"Login attempt with invalid email: {user_credentials.email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    logger.info(f"User found: {db_user.email}")
    
    if not utils.verify_password(user_credentials.password, db_user.hashed_password):
        logger.warning(f"Invalid password for email: {user_credentials.email}")
        logger.info(f"Stored hashed password: {db_user.hashed_password}")
        logger.info(f"Provided password: {user_credentials.password}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    logger.info(f"User logged in: {user_credentials.email}")
    return {"access_token": access_token, "token_type": "bearer"}


# Search for books via Google Books API (public route, no authentication required)
@app.get("/search_books/")
def search_books(book_name: str, author_name: str):
    try:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={book_name}+inauthor:{author_name}&key={API_KEY}")
        response.raise_for_status()  # Raise an error for bad responses
        logger.info(f"Book search performed: {book_name} by {author_name}, Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise HTTPException(status_code=500, detail="HTTP error occurred")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        raise HTTPException(status_code=500, detail="An error occurred")
# Save a book to user's profile (requires authentication)

@app.post("/users/{user_id}/books/")
def save_book(
    user_id: int, 
    book: schemas.Book, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(get_current_user)
):
    user = crud.get_user_by_id(db, user_id=user_id)
    if not user:
        logger.error(f"Attempt to save book for non-existent user: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id != current_user.id:
        logger.warning(f"Unauthorized book save attempt by user: {current_user.id} for user: {user_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot add books to another user's profile")
    
    added_book = crud.add_book_to_user(db, user=user, book=book)
    logger.info(f"Book added to user profile: {user_id}, Book title: {book.title}")
    return added_book

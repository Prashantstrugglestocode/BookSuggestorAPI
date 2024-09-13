import logging
from sqlalchemy.orm import Session
from . import models, schemas
from . import utils

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

def get_user_by_email(email: str, db: Session) -> models.User:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        logger.info(f"User found by email: {email}")
    else:
        logger.info(f"No user found by email: {email}")
    return user

def create_user(user: schemas.UserCreate, db: Session) -> models.User:
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def add_book_to_user(user: models.User, book: schemas.Book, db: Session) -> models.Book:
    db_book = models.Book(**book.dict())
    user.books.append(db_book)
    db.commit()
    logger.info(f"Book added to user profile: {user.id}, Book title: {book.title}")
    return db_book

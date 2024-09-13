from sqlalchemy import Column, Integer, String, ForeignKey, Table
from .database import Base

# Fix: Include Base.metadata in the table definition
user_books = Table(
    'user_books', Base.metadata,  # Pass Base.metadata here
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('book_id', ForeignKey('books.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, unique=True, index=True, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=False)

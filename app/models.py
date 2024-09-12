from sqlalchemy import Column,Integer,String,ForeignKey,Table
from sqlalchemy.orm import relationship
from .database import Base



user_books = Table(
        'user_books', Base.metadata,
        Column('user_id', ForeignKey('users.id')),
        Column('book_id', ForeignKey('books.id'))
        )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True,nullable=False)
    email=Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    books = relationship("Book", secondary=user_books ,back_populates="users")


    class Book(Base):
        __tablename__ = 'books'
       
       
        id = Column(Integer, primary_key=True,nullable=False,index=True)
        title = Column(String, unique=True, index=True, nullable=False)
        author = Column(String, nullable=False)
        description = Column(String, nullable=False)
        users = relationship("User", secondary=user_books ,back_populates="books")
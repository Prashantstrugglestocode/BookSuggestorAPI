from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()



DB_USERNAME= os.getenv('DB_USERNAME')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_TABLE=os.getenv('DB_TABLE')
HOST=os.getenv('HOST')


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{HOST}/{DB_TABLE}"
print(SQLALCHEMY_DATABASE_URL)
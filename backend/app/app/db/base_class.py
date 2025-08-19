from typing import Any
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from sqlalchemy.orm import declarative_base

load_dotenv()
Base=declarative_base()


# db_url="mysql+pymysql://root:2741@localhost:3307/capstone_school_db"
db_url=os.getenv("DATABASE_URL")

engine=create_engine(db_url)

Session=sessionmaker(bind=engine)



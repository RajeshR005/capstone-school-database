from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from sqlalchemy.orm import declarative_base

Base=declarative_base()


db_url="mysql+pymysql://root:2741@localhost:3307/capstone_school_db"

engine=create_engine(db_url)

Session=sessionmaker(bind=engine)

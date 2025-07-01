
from typing import Generator
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.base_class import Session
from app.core.config import settings


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token")

"""Initializing the database Connection"""
def get_db() -> Generator:
    try:
        db = Session()
        yield db
    finally:
        db.close()


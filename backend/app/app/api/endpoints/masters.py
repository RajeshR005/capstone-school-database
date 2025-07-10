from fastapi import APIRouter, Depends, Form,requests
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import get_db,check_token_all,check_token
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from app.schemas import user_schema,login_schema,attendance_schema
from typing import Optional
from app.crud import section_crud,standard_crud,classroom_crud,subject_crud,academic_crud,group_crud,exam_crud,term_crud
api_router=APIRouter(prefix="/masters")

api_router.include_router(standard_crud.router,tags=["Master's Standard"])
api_router.include_router(section_crud.router,tags=["Master's Section"])

api_router.include_router(subject_crud.router,tags=["Master's Subject"])
api_router.include_router(academic_crud.router,tags=["Master's Academic Year"])
api_router.include_router(group_crud.router,tags=["Master's Group "])
api_router.include_router(exam_crud.router,tags=["Masters's Exam"])
api_router.include_router(term_crud.router,tags=["Master's Term"])

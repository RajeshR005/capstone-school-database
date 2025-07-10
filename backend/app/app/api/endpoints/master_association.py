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
from app.crud import section_crud,standard_crud,classroom_crud,subject_crud,academic_crud,group_crud,class_academic_crud,subject_alloc_crud,exam_alloc_crud,student_class_crud
api_router=APIRouter(prefix="/masters_association")

api_router.include_router(classroom_crud.router,tags=["Master's Classroom Allocation"])
api_router.include_router(class_academic_crud.router,tags=["Master's Class Academic Allocation"])
api_router.include_router(subject_alloc_crud.router,tags=["Master's Subject Allocation"])
api_router.include_router(exam_alloc_crud.router,tags=["Master's Exam Allocation"])
api_router.include_router(student_class_crud.router,tags=["Master's Student Class Allocation"])

from fastapi import APIRouter, Depends, Form,requests
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from app.schemas import user_schema,login_schema
from typing import Optional

router=APIRouter()

@router.post("/Add_students_attendance",description="The Staffs can Add their Student Attendance")
def add_student_attendance(present_id:Optional[list[int]]=Form(None),Absent_id:Optional[list[int]]=Form(None),Half_morning:Optional[list[int]]=Form(None),Half_afternoon:Optional[list[int]]=Form(None),On_duty:Optional[list[int]]=Form(None),Attendance_date:date=Form(...),Check_in_time:time=Form(None),Check_out_time:time=Form(None),db:Session=Depends(get_db),current_user:User=Depends(create_access_token)):
    attendance_users=[(present_id,1),(Absent_id,0),(Half_morning,2),(Half_afternoon,3),(On_duty,4)]
    for user_id,status in attendance_users:
        user_id=user_id,
        attendance_date=Attendance_date,
        status=status
        check_in=Check_in_time,
        check_out=Check_out_time,
        created_by=

        
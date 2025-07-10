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
router=APIRouter()



@router.post('/add_exam',description="This Route is for Adding Data in the Exam table")
def add_exam(token:str=Form(...),exam_name:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_data=db.query(Exam).filter(Exam.exam_name==exam_name.title(),Exam.status==1).first()
    if get_data:
        return{"status":0,"msg":f"The Provided Already exists in the Database "}
    exam_name_title=exam_name.title()
    add_data=Exam(
        exam_name=exam_name_title,
        created_by=get_admin.id,
        modified_by=get_admin.id
    )
    db.add(add_data)
    db.commit()
    return{"status":1,"msg":f"{exam_name.title()} Added Successfully in the Database"}

@router.post('/list_exam_data_active',description="This Route is used to View the Active Exam's Data in the DB")
def list_exam_data_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_data=db.query(Exam).filter(Exam.status==1).all()
    if not view_data:
        return{"status":0,"msg":"No Active Exam Data Available in the DB"}
    return view_data

@router.post('/list_exam_data_in_active',description="This Route is used to View the In-Active Exam's Data in the DB")
def list_exam_data_in_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_data=db.query(Exam).filter(Exam.status==-1).all()
    if not view_data:
        return{"status":0,"msg":"No In-Active Exam Data Available in the DB"}
    return view_data

@router.post('/change_status_exam',description="This Route is for change status of  Data in the Exam table")
def change_status_exam(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_data=db.query(Exam).filter(Exam.id==id).first()
    if not change_status_data:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_data.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_data.exam_name} Activated Sucessful"}
    elif change_status==2:
        return{"status":1,"msg":f"{change_status_data.exam_name} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_data.exam_name} In-Activated Sucessful"}
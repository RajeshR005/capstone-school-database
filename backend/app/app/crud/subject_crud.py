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

@router.post('/add_subject',description="This Route is for Adding Data in the Subject table")
def add_subject(token:str=Form(...),Subject_name:str=Form(...),Subject_code:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_sub=db.query(Subject).filter(Subject.subject_name==Subject_name.capitalize(),Subject.code==Subject_code,Subject.status==1).first()
    if get_sub:
        return{"status":0,"msg":f"The {Subject_name.capitalize()} with {Subject_code} Already exists in the Database "}
    subject_cp=Subject_name.capitalize()
    add_sub=Subject(
        subject_name=subject_cp,
        code=Subject_code,
        created_by=get_admin.id,
        modified_by=get_admin.id
    )
    db.add(add_sub)
    db.commit()
    return{"status":1,"msg":f"{Subject_name.capitalize()} with {Subject_code} Added Successfully in the Database"}

@router.post('/edit_subject',description="This Route is for Editing the Data of the Subject table in the Database ")
def edit_subject(token:str=Form(...),subj_id:int=Form(...),modify_subject:Optional[str]=Form(None),modify_subject_code:Optional[str]=Form(None),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_subject=db.query(Subject).filter(Subject.id==subj_id,Subject.status==1)
    get_sub_instance=get_subject.first()
    if not get_sub_instance:
        return{"status":0,"msg":f"There is no Data available for this Subject ID: {subj_id}"}
    if modify_subject =="string" and modify_subject_code == "string":
        return{"status":0,"msg":"There is no data provided for the update"}
    subj_name_cp=modify_subject.capitalize()
    if modify_subject:
        get_sub_instance.subject_name=subj_name_cp
    if modify_subject_code:
        get_sub_instance.code=modify_subject_code
    db.commit()
    return {"status":1,"msg":f"Data Updated Successfully for the Subject ID: {subj_id}"}

@router.post('/list_subject_data_active',description="This Route is used to View the Active Subject Data in the DB")
def list_subject_data_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_sub=db.query(Subject).filter(Subject.status==1).all()
    if not view_sub:
        return{"status":0,"msg":"No Active Subject Data Available in the DB"}
    return view_sub

@router.post('/list_subject_data_in_active',description="This Route is used to View the In-Active Subject Data in the DB")
def list_subject_data_in_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_sub=db.query(Subject).filter(Subject.status==-1).all()
    if not view_sub:
        return{"status":0,"msg":"No In-Active Subject Data Available in the DB"}
    return view_sub

@router.post('/change_status_subject',description="This Route is for change status of  Data in the Subject table")
def change_status_subject(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_sub=db.query(Subject).filter(Subject.id==id).first()
    if not change_status_sub:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_sub.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_sub.id} Activated Sucessful"}
    elif change_status==2:
        return{"status":1,"msg":f"{change_status_sub.id} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_sub.id} In-Activated Sucessful"}
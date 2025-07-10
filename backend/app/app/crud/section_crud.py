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

@router.post('/add_section',description="This Route is used for Adding Data in Section Table ")
def add_section(token:str=Form(...),section_name:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    check_section=db.query(Section).filter(Section.section_name==section_name.upper(),Section.status==1).first()
    if check_section:
        return{"status":0,"msg":f"{section_name} Already Exists in the Database"}
    section_up=section_name.upper()
    add_section_data=Section(
        section_name=section_up,
        created_by=get_admin.id,
        modified_by=get_admin.id
    )
    print(section_name.upper())
    db.add(add_section_data)
    db.commit()
    return{"status":0,"msg":f"{section_name.capitalize()} Added Successfully in the Database"}

@router.post('/list_section_data_active',description="This Route is used to View the Active Section's Data in the DB")
def list_section_data_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_section=db.query(Section).filter(Section.status==1).all()
    if not view_section:
        return{"status":0,"msg":"No Section Data Available in the DB"}
    return view_section

@router.post('/list_section_data_in_active',description="This Route is used to View the Inactive Section's Data in the DB")
def list_section_data_in_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_section=db.query(Section).filter(Section.status==-1).all()
    if not view_section:
        return{"status":0,"msg":"No In-Active Section Data Available in the DB"}
    return view_section

@router.post('/change_status_section',description="This Route is for change status of Data in the Section table")
def change_status_section(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_sec=db.query(Section).filter(Section.id==id).first()
    if not change_status_sec:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_sec.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_sec.section_name} Activated Sucessful"}
    elif change_status==0:
        return{"status":1,"msg":f"{change_status_sec.section_name} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_sec.section_name} In-Activated Sucessful"}
    
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

@router.post('/add_standard',description="This Route is for Adding Data in the Standard table")
def add_standard(token:str=Form(...),Standard_name:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_std=db.query(Standard).filter(Standard.std_name==Standard_name.lower(),Standard.status==1).first()
    if get_std:
        return{"status":0,"msg":f"The {Standard_name} Already exists in the Database "}
    standard_low=Standard_name.lower()
    add_std=Standard(
        std_name=standard_low,
        created_by=get_admin.id,
        modified_by=get_admin.id
    )
    db.add(add_std)
    db.commit()
    return{"status":1,"msg":f"{Standard_name} Added Successfully in the Database"}

@router.post('/list_standard_data_active',description="This Route is used to View the Active Standard's Data in the DB")
def list_standard_data_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_standard=db.query(Standard).filter(Standard.status==1).all()
    if not view_standard:
        return{"status":0,"msg":"No Active-Standard Data Available in the DB"}
    return view_standard

@router.post('/list_standard_data_in_active',description="This Route is used to View the In-Active Standard's Data in the DB")
def list_standard_data_in_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_standard=db.query(Standard).filter(Standard.status==-1).all()
    if not view_standard:
        return{"status":0,"msg":"No In-active Standard Data Available in the DB"}
    return view_standard

@router.post('/change_status_standard',description="This Route is for change status of  Data in the Standard table")
def change_status_standard(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_std=db.query(Standard).filter(Standard.id==id).first()
    if not change_status_std:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_std.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_std.std_name} Activated Sucessful"}
    elif change_status==2:
        return{"status":1,"msg":f"{change_status_std.std_name} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_std.std_name} In-Activated Sucessful"}
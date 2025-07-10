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

@router.post('/add_classroom',description="This Route is for Adding the Data in the Classroom with section and standard data")
def add_classroom(token:str=Form(...),standard_name:str=Form(...),section_name:str=Form(...),class_advisor_id:int=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_standard=db.query(Standard).filter(Standard.std_name==standard_name.lower(),Standard.status==1).first()
    if not get_standard:
        return{"status":0,"msg":"The provided Standard name doesn't exist in the Database"}
    get_section=db.query(Section).filter(Section.section_name==section_name.upper(),Section.status==1).first()
    if not get_section:
        return{"status":0,"msg":"The provided Section name doesn't exist in the Database"}
    check_classroom=db.query(Classroom).filter(Classroom.standard_id==get_standard.id,Classroom.section_id==get_section.id,Classroom.class_advisor_id==class_advisor_id,Classroom.status==1).first()
    if check_classroom:
        return{"status":0,"msg":"This Classroom Data Already Exist in the Database"}
    
    add_classroom_data=Classroom(
        standard_id=get_standard.id,
        section_id=get_section.id,
        class_advisor_id=class_advisor_id,
        created_by=get_admin.id,
        modified_by=get_admin.id

    )
    db.add(add_classroom_data)
    db.commit()
    db.refresh(add_classroom_data)
    return{"status":1,"msg":f"Classroom data Added Successfully class_id: {add_classroom_data.id}"}

@router.post('/edit_classroom',description="This Route is for Editing the Data of the Classroom in the Database ")
def edit_classroom(token:str=Form(...),classroom_id:int=Form(...),modify_standard:Optional[int]=Form(None),modify_section:Optional[int]=Form(None),modify_class_advisor:Optional[int]=Form(None),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_classroom=db.query(Classroom).filter(Classroom.id==classroom_id,Classroom.status==1)
    get_cls_instance=get_classroom.first()
    if not get_cls_instance:
        return{"status":0,"msg":f"There is no Data available for this class id: {classroom_id}"}
    if modify_standard is 0 and modify_section is 0 and modify_class_advisor is 0:
        return{"status":0,"msg":"There is no data provided for the update"}
    if modify_standard:
        get_cls_instance.standard_id=modify_standard
    if modify_section:
        get_cls_instance.section_id=modify_section
    if modify_class_advisor:
        get_cls_instance.class_advisor_id=modify_class_advisor
    db.commit()
    return {"status":1,"msg":f"Data Updated Successfully for the Class ID {classroom_id}"}

@router.post('/list_classroom_data_active',description="This Route is used to View the Active classroom Data in the DB")
def list_classroom_active_data(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_classroom=db.query(Classroom).filter(Classroom.status==1).all()
    if not view_classroom:
        return{"status":0,"msg":"No Active Classroom Data Available in the DB"}
    return view_classroom

@router.post('/list_classroom_data_in_active',description="This Route is used to View the In-Active classroom Data in the DB")
def list_classroom_in_active_data(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_classroom=db.query(Classroom).filter(Classroom.status==-1).all()
    if not view_classroom:
        return{"status":0,"msg":"No In-Active Classroom Data Available in the DB"}
    return view_classroom

@router.post('/change_status_Classroom',description="This Route is for change status of Data in the Classroom table")
def change_status_classroom(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_cls=db.query(Classroom).filter(Classroom.id==id).first()
    if not change_status_cls:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_cls.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_cls.id} Activated Sucessful"}
    elif change_status==0:
        return{"status":1,"msg":f"{change_status_cls.id} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_cls.id} In-Activated Sucessful"}
    
    
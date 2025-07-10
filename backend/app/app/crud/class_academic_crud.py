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

@router.post('/add_class_academic_associations',description="This Route is for Adding the Data in the Class with Academic and group id")
def add_class_academic_associations(token:str=Form(...),Classroom_id:int=Form(...),Academic_year_id:int=Form(...),group_id:Optional[int]=Form(None),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    check_classroom=db.query(Classroom).filter(Classroom.id==Classroom_id,Classroom.status==1).first()
    if not check_classroom:
        return{"status":0,"msg":"This Classroom Data Doesn't Exist in the Database"}
    check_academic=db.query(AcademicYear).filter(AcademicYear.id==Academic_year_id,AcademicYear.status==1).first()
    if not check_academic:
        return{"status":0,"msg":"This Academic Data Doesn't Exist in the Database"}
    if group_id not in [None, 0]:
        check_group_id=db.query(Group).filter(Group.id==group_id,Group.status==1).first()
        if not check_group_id:
            return{"status":0,"msg":"This Group Data Doesn't Exist in the Database"}
    
    
    get_cls_acad=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.classroom_id==Classroom_id,ClassAcademicAssociation.status==1).first()
    if get_cls_acad:
        return{"status":0,"msg":"This Classroom Association Data Already Exist in the Database"}
    
    add_classroom_assoc_data=ClassAcademicAssociation(
        classroom_id=Classroom_id,
        academic_year_id=Academic_year_id,
        group_id=group_id if group_id not in [0, None] else None,
        created_by=get_admin.id,
        modified_by=get_admin.id

    )
    db.add(add_classroom_assoc_data)
    db.commit()
    db.refresh(add_classroom_assoc_data)
    return{"status":1,"msg":f"Classroom with associate data Added Successfully class_Associate_id: {add_classroom_assoc_data.id}"}

@router.post('/edit_class_academic_associations',description="This Route is for Editing the Data of the Classroom with Associate in the Database ")
def edit_class_academic_associations(token:str=Form(...),classroom_assoc_id:int=Form(...),modify_classroom_id:Optional[int]=Form(None),modify_academic_year_id:Optional[int]=Form(None),modify_group_id:Optional[int]=Form(None),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_cls_acad=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.id==classroom_assoc_id,ClassAcademicAssociation.status==1)
    get_cls_acad_instance=get_cls_acad.first()
    if not get_cls_acad_instance:
        return{"status":0,"msg":f"There is no Data available for this class Association id: {classroom_assoc_id}"}
    if modify_classroom_id is 0 and modify_academic_year_id is 0 and modify_group_id is 0:
        return{"status":0,"msg":"There is no data provided for the update"}
    if modify_classroom_id:
        get_cls_acad_instance.classroom_id=modify_classroom_id
    if modify_academic_year_id:
        get_cls_acad_instance.academic_year_id=modify_academic_year_id
    if modify_group_id:
        get_cls_acad_instance.group_id=modify_group_id
    db.commit()
    return {"status":1,"msg":f"Data Updated Successfully for the Class Associate ID {classroom_assoc_id}"}

@router.post('/list_class_academic_associations_data_active',description="This Route is used to View the Active classroom Associate Data in the DB")
def list_classroom_active_data(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_cls_acad=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.status==1).all()
    if not view_cls_acad:
        return{"status":0,"msg":"No Active Class Academic Data Available in the DB"}
    return view_cls_acad

@router.post('/list_class_academic_associations_data_in_active',description="This Route is used to View the In-Active classroom Associate Data in the DB")
def list_classroom_in_active_data(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_cls_acad=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.status==-1).all()
    if not view_cls_acad:
        return{"status":0,"msg":"No In-Active Class Academic Data Available in the DB"}
    return view_cls_acad

@router.post('/change_status_class_academic_associations',description="This Route is for change status of Data in the Classroom Associate table")
def change_status_classroom(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_cls_acad=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.id==id).first()
    if not change_status_cls_acad:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_cls_acad.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_cls_acad.id} Activated Sucessful"}
    elif change_status==0:
        return{"status":1,"msg":f"{change_status_cls_acad.id} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_cls_acad.id} In-Activated Sucessful"}
    
    

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


@router.post('/add_subject_allocate',description="This Route is for Adding the Subject Allocation Data")
def add_subject_allocate(token:str=Form(...),Class_academic_id:int=Form(...),subject_id:int=Form(...),staff_id:int=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_cls_acad=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.id==Class_academic_id,ClassAcademicAssociation.status==1).first()
    if not get_cls_acad:
        return{"status":0,"msg":"The provided Class Academic ID doesn't exist in the Database"}
    get_subject=db.query(Subject).filter(Subject.id==subject_id,Subject.status==1).first()
    if not get_subject:
        return{"status":0,"msg":"The provided Subject ID doesn't exist in the Database"}
    staff_data=db.query(User).filter(User.id==staff_id,User.role=="staff").first()
    if not staff_data:
        return{"status":0,"msg":"This Staff ID doesn't Exist in the Database"}
    get_subj_alloc=db.query(SubjectAllocation).filter(SubjectAllocation.class_academic_id==Class_academic_id,SubjectAllocation.subject_id==subject_id,SubjectAllocation.staff_id==staff_id,SubjectAllocation.status==1).first()
    if get_subj_alloc:
        return{"status":0,"msg":"The Subject Allocation Data Already Exists in the Database"}
    add_subject_alloc_data=SubjectAllocation(
        class_academic_id=Class_academic_id,
        subject_id=subject_id,
        staff_id=staff_id,
        created_by=get_admin.id,
        modified_by=get_admin.id

    )
    db.add(add_subject_alloc_data)
    db.commit()
    db.refresh(add_subject_alloc_data)
    return{"status":1,"msg":f"Subject Allocate data Added Successfully : {add_subject_alloc_data.id}"}

@router.post('/edit_subject_allocate',description="This Route is for Editing the Data of the Subject Allocate in the Database ")
def edit_subject_allocate(token:str=Form(...),subj_allocate_id:int=Form(...),modify_classroom_academic_id:Optional[int]=Form(None),modify_subject:Optional[int]=Form(None),modify_staff:Optional[int]=Form(None),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_subj_alloc=db.query(SubjectAllocation).filter(SubjectAllocation.id==subj_allocate_id,SubjectAllocation.status==1)
    get_subj_alloc_instance=get_subj_alloc.first()
    if not get_subj_alloc_instance:
        return{"status":0,"msg":f"There is no Data available for this Subject Allocation id: {subj_allocate_id}"}
    if modify_classroom_academic_id ==0 and modify_subject == 0 and modify_staff == 0:
        return{"status":0,"msg":"There is no data provided for the update"}
    if modify_classroom_academic_id:
        get_subj_alloc_instance.class_academic_id=modify_classroom_academic_id
    if modify_subject:
        get_subj_alloc_instance.subject_id=modify_subject
    if modify_staff:
        get_subj_alloc_instance.staff_id=modify_staff
    db.commit()
    return {"status":1,"msg":f"Data Updated Successfully for the Subject Allocation {subj_allocate_id}"}

@router.post('/list_subject_allocate_data_active',description="This Route is used to View the Active subject_allocate Data in the DB")
def list_subject_allocate_active_data(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_subj_alloc=db.query(SubjectAllocation).filter(SubjectAllocation.status==1).all()
    if not view_subj_alloc:
        return{"status":0,"msg":"No Active subject Allocate Data Available in the DB"}
    return view_subj_alloc

@router.post('/list_subject_allocate_data_in_active',description="This Route is used to View the In-Active subject_allocate Data in the DB")
def list_subject_allocate_in_active_data(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_subj_alloc=db.query(SubjectAllocation).filter(SubjectAllocation.status==-1).all()
    if not view_subj_alloc:
        return{"status":0,"msg":"No In Active Subject Allocate Data Available in the DB"}
    return view_subj_alloc

@router.post('/change_status_subject_allocate',description="This Route is for change status of Data in the subject Allocate table")
def change_status_subject_allocate(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_subj_alloc=db.query(SubjectAllocation).filter(SubjectAllocation.id==id).first()
    if not change_status_subj_alloc:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_subj_alloc.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_subj_alloc.id} Activated Sucessful"}
    elif change_status==0:
        return{"status":1,"msg":f"{change_status_subj_alloc.id} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_subj_alloc.id} In-Activated Sucessful"}
    
    
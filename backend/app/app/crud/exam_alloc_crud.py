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


@router.post('/add_exam_allocate',description="This Route is for Adding the Exam Allocation Data")
def add_exam_allocate(token:str=Form(...),standard_id:int=Form(...),exam_id:int=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_data_std=db.query(Standard).filter(Standard.id==standard_id,Standard.status==1).first()
    if not get_data_std:
        return{"status":0,"msg":"The provided standard data doesn't exist in the Database"}
    get_data_exam=db.query(Exam).filter(Exam.id==exam_id,Exam.status==1).first()
    if not get_data_exam:
        return{"status":0,"msg":"The provided Exam ID doesn't exist in the Database"}
    if get_data_std.std_name in ["11", "12"]:
        if not group_id or group_id == 0:
            return {"status": 0, "msg": "Group is mandatory for standard 11 and 12"}
        check_group = db.query(Group).filter(Group.id == group_id, Group.status == 1).first()
        if not check_group:
            return {"status": 0, "msg": "This Group Data Doesn't Exist in the Database"}
    else:
        group_id = None
    
    get_exam_alloc=db.query(ExamAllocation).filter(ExamAllocation.standard_id==standard_id,ExamAllocation.exam_id==exam_id,ExamAllocation.status==1).first()
    if get_exam_alloc:
        return{"status":0,"msg":"The Exam Allocation Data Already Exists in the Database"}
    add_exam_alloc_data=ExamAllocation(
        standard_id=standard_id,
        group_id=group_id if group_id not in [0, None] else None,
        exam_id=exam_id,
        created_by=get_admin.id,
        modified_by=get_admin.id

    )
    db.add(add_exam_alloc_data)
    db.commit()
    db.refresh(add_exam_alloc_data)
    return{"status":1,"msg":f"Subject Allocate data Added Successfully : {add_exam_alloc_data.id}"}

@router.post('/edit_exam_allocate',description="This Route is for Editing the Data of the Exam Allocate in the Database ")
def edit_exam_allocate(token:str=Form(...),exam_allocate_id:int=Form(...),modify_standard_id:Optional[int]=Form(None),modify_exam_id:Optional[int]=Form(None),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_exam_alloc=db.query(ExamAllocation).filter(ExamAllocation.id==exam_allocate_id,ExamAllocation.status==1)
    get_exam_alloc_instance=get_exam_alloc.first()
    if not get_exam_alloc_instance:
        return{"status":0,"msg":f"There is no Data available for this Exam Allocation id: {exam_allocate_id}"}
    if modify_standard_id ==0 and  modify_exam_id == 0:
        return{"status":0,"msg":"There is no data provided for the update"}
    if modify_standard_id:
        get_exam_alloc_instance.standard_id=modify_standard_id
    if modify_exam_id:
        get_exam_alloc_instance.exam_id=modify_exam_id
    db.commit()
    return {"status":1,"msg":f"Data Updated Successfully for the Exam Allocation {exam_allocate_id}"}

@router.post('/list_exam_allocate_data_active',description="This Route is used to View the Active Exam Allocate Data in the DB")
def list_exam_allocate_active_data(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_data_alloc=db.query(ExamAllocation).filter(ExamAllocation.status==1).all()
    if not view_data_alloc:
        return{"status":0,"msg":"No Active Exam Allocate Data Available in the DB"}
    return view_data_alloc

@router.post('/list_exam_allocate_data_in_active',description="This Route is used to View the In-Active Exam Allocate Data in the DB")
def list_exam_allocate_in_active_data(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_data_alloc=db.query(ExamAllocation).filter(ExamAllocation.status==-1).all()
    if not view_data_alloc:
        return{"status":0,"msg":"No In Active Exam Allocate Data Available in the DB"}
    return view_data_alloc

@router.post('/change_status_Exam_allocate',description="This Route is for change status of Data in the Exam Allocate table")
def change_status_Exam_allocate(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_data_alloc=db.query(ExamAllocation).filter(ExamAllocation.id==id).first()
    if not change_status_data_alloc:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_data_alloc.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_data_alloc.id} Activated Sucessful"}
    elif change_status==0:
        return{"status":1,"msg":f"{change_status_data_alloc.id} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_data_alloc.id} In-Activated Sucessful"}
    
    
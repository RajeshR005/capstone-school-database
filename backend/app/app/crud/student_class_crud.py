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
from typing import List, Optional
router=APIRouter()


@router.post('/add_students_class', description="This Route is used to Add multiple students in a class academic id")
def add_students_class(field: user_schema.StudentClassList, db: Session = Depends(get_db)):
    get_admin = check_token(field.token, db)
    if isinstance(get_admin, dict):
        return get_admin
    if get_admin.role != "admin":
        return {"status": 0, "msg": "You are not authorized here"}
    class_acad = db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.id == field.class_academic_year_id,ClassAcademicAssociation.status == 1).first()
    if not class_acad:
        return {"status": 0, "msg": " The provided Class Academic ID not in the Databae"}
    get_stu_all=db.query(User).filter(User.role=="student").all()
    valid_stu=[]
    for i in get_stu_all:
        valid_stu.append(i.id)
    inserted = []
    not_inserted=[]
    for student in field.students_data:
        student_id = student.student_id
        roll_number = student.roll_number
        if student_id not in valid_stu:
            return{"status":0,"msg":"The Provided Student Data is not Valid student ID"}
        existing = db.query(StudentClass).filter(StudentClass.class_academic_id == field.class_academic_year_id,StudentClass.student_id == student_id,StudentClass.status == 1).first()
        if existing:
            not_inserted.append(student.student_id)
            continue
        add_data = StudentClass(
            student_id=student_id,
            class_academic_id=field.class_academic_year_id,
            roll_number=roll_number,
            created_by=get_admin.id,
            modified_by=get_admin.id
        )
        db.add(add_data)
        inserted.append(student_id)

    db.commit()

    return {"status": 1,"msg": f"These Students data {inserted} Updated Successful","msg2": f"These Students data {not_inserted} Already Exist with this {field.class_academic_year_id}"}

@router.post('/list_student_class_data_active',description="This Route is used to View the Active Student class Data in the DB")
def list_student_class_data_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_data=db.query(StudentClass).filter(StudentClass.status==1).all()
    if not view_data:
        return{"status":0,"msg":"No Active Student Class Data Available in the DB"}
    return view_data

@router.post('/list_student_class_data_in_active',description="This Route is used to View the In Active Exam's Data in the DB")
def list_student_class_data_in_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_data=db.query(StudentClass).filter(StudentClass.status==-1).all()
    if not view_data:
        return{"status":0,"msg":"No In-Active Student Class Data Available in the DB"}
    return view_data

@router.post('/change_status_student_class',description="This Route is for change the student Status in the Academic Class to change to another Class ")
def change_status_student_class(token:str=Form(...),student_class_id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin = check_token(token, db)
    if isinstance(get_admin, dict):
        return get_admin
    if get_admin.role != "admin":
        return {"status": 0, "msg": "You are not authorized here"}
    change_status_data=db.query(StudentClass).filter(StudentClass.id==student_class_id).first()
    if not change_status_data:
        return{"status":0,"msg":"The Student Class Id is not exist in the Database"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_data.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_data.id} Activated Sucessful"}
    elif change_status==2:
        return{"status":1,"msg":f"{change_status_data.id} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_data.id} In-Activated Sucessful"}
from fastapi import APIRouter, Depends, Form,requests
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import get_db,check_token_all
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from app.schemas import user_schema,login_schema,attendance_schema
from typing import Optional

router=APIRouter(prefix="/staff")

@router.post("/view_students",description="The Staffs can View their students details in their class")
def view_students(token:str=Form(...),db:Session=Depends(get_db)):
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if not get_user.role=="staff":
        return{"status":0,"msg":"Only Staff's can View Student's in their class"}
    get_staff_cls=db.query(Classroom).filter(Classroom.class_advisor_id==get_user.id).first()
    if not get_staff_cls:
        return{"status":0,"msg":"No Class is Associated with this Staff"}
    get_cls_acad_id=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.classroom_id==get_staff_cls.id).first()
    get_students=db.query(StudentClass).filter(StudentClass.class_academic_id==get_cls_acad_id.id).all()
    if not get_students:
        return{"status":0,"msg":"There is no Student Data Available for this Class"}
    view_students=[]
    for i in get_students:
        view_students_data=db.query(StudentClass,User).join(StudentClass.student).filter(i.student_id==User.id).first()
        view_students.append(view_students_data)
    return [

        {   "student_id":i.User.id,
            "First Name":i.User.first_name,
            "Last Name":i.User.last_name,
            "Roll No":i.StudentClass.roll_number,
            "Date of Birth":i.User.date_of_birth,
            "Email":i.User.email,
            "phone number":i.User.phone_number,
            "Blood group":i.User.blood_group,
            "Aadhaar Number":i.User.aadhaar_num,
            "Umis No":i.User.umis_no,
            "Father Name":i.User.father_name,
            "Mother Name":i.User.mother_name,
            "Parent phone":i.User.parent_phone,
            "Emergency Number":i.User.emergency_num,
        }
        for i in view_students

    ]
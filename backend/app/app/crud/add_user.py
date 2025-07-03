from fastapi import APIRouter, Depends, Form,requests
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from app.schemas import user_schema,login_schema

import random



router = APIRouter()


# @router.post('/create_admin',description="This Route is for Creating Admin Data")
# def admin_user(admin:user_schema.Admin_data,db:Session=Depends(get_db),current_user:User=Depends(create_access_token)):
#     if current_user.role=="admin":
#             check_duplicate=db.query(User).filter(User.email==admin.email,User.status==1).first()
#             if check_duplicate:
#                   return{"status":0,"msg":"User Data Already Exists"}
#             create_admin=User(
#                 email=admin.email,
#                 password=get_password_hash(admin.password),
#                 role="admin",
#                 created_by=current_user.id,
#                 modified_by=current_user.id
#             )    
#             db.add(create_admin)
#             db.commit()
#             return{"status":1,"msg":"Admin profile Created Sucessfully"}
            
#     else:
#         return{"status":0,"msg":"You are Not Authorized to Access"}
    
# @router.post('/create_staff',description="This Route is for Creating Staff Data")
# def staff_user(staff:user_schema.staff_data,db:Session=Depends(get_db),current_user:User=Depends(create_access_token)):
#     if current_user.role=="admin":
#             check_duplicate=db.query(User).filter(User.email==staff.email,User.status==1).first()
#             if check_duplicate:
#                   return{"status":0,"msg":"User Data Already Exists"}
#             create_address=Address(
#                 current_address=staff.address.current_address,
#                 current_city=staff.address.current_city,
#                 current_pincode=staff.address.current_pincode,
#                 permanent_address=staff.address.permanent_address,
#                 permanent_city=staff.address.permanent_city,
#                 permanent_pincode=staff.address.permanent_pincode,
#                 state=staff.address.state,
#                 country=staff.address.country,
#                 created_by=current_user.id,
#                 modified_by=current_user.id

#             )
#             db.add(create_address)
#             db.commit()
#             db.refresh(create_address)
#             create_staff=User(
#                 first_name=staff.first_name,
#                 last_name=staff.last_name,
#                 date_of_birth=staff.date_of_birth,
#                 gender=staff.gender,
#                 role="staff",
#                 email=staff.email,
#                 password=get_password_hash(staff.password),
#                 phone_number=staff.phone_number,
#                 blood_group=staff.blood_group,
#                 aadhaar_num=staff.aadhaar_num,
#                 emergency_num=staff.emergency_num,
#                 date_of_join=staff.date_of_join,
#                 address_id=create_address.id,
#                 created_by=current_user.id,
#                 modified_by=current_user.id

#             )
#             db.add(create_staff)
#             db.commit()
#             return{"status":1,"msg":"Staff profile Created Sucessfully"}
#     else:
#          return{"status":0,"msg":"You are Not Authorized to Access"}
    
@router.post('/create_student',description="This Route is for Creating Student Data")
def student_user(student:user_schema.Student_data,db:Session=Depends(get_db),current_user:User=Depends(create_access_token)):
    if current_user.role in ["staff", "admin"]:
            check_duplicate=db.query(User).filter(User.email==student.email,User.status==1).first()
            if check_duplicate:
                  return{"status":0,"msg":"User Data Already Exists"}
            create_address=Address(
                current_address=student.address.current_address,
                current_city=student.address.current_city,
                current_pincode=student.address.current_pincode,
                permanent_address=student.address.permanent_address,
                permanent_city=student.address.permanent_city,
                permanent_pincode=student.address.permanent_pincode,
                state=student.address.state,
                country=student.address.country,
                created_by=current_user.id,
                modified_by=current_user.id

            )
            db.add(create_address)
            db.commit()
            db.refresh(create_address)
            create_student=User(
                first_name=student.first_name,
                last_name=student.last_name,
                date_of_birth=student.date_of_birth,
                gender=student.gender,
                role="student",
                email=student.email,
                password=get_password_hash(student.password),
                phone_number=student.phone_number,
                blood_group=student.blood_group,
                mother_tongue=student.mother_tongue,
                aadhaar_num=student.aadhaar_num,
                is_hosteller=student.is_hosteller,
                specially_abled_person=student.specially_abled_person,
                umis_no=student.umis_no,
                father_name=student.father_name,
                mother_name=student.mother_name,
                parent_phone=student.parent_phone,
                emergency_num=student.emergency_num,
                date_of_join=student.date_of_join,
                address_id=create_address.id,
                created_by=current_user.id,
                modified_by=current_user.id

            )
            db.add(create_student)
            db.commit()
            return{"status":1,"msg":"Student profile Created Sucessfully"}
    else:
         return{"status":0,"msg":"You are Not Authorized to Access"}

          
          





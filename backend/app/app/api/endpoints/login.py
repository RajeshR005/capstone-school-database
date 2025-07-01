
from fastapi import APIRouter, Depends, Form,requests
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from app.schemas import user_schema,login_schema

import random


router = APIRouter()


# @router.post("/create_user")
# async def signup_user(field:user_schema.Create_user,db:Session=Depends(deps.get_db)):
#     check_user=db.query()
    
#     get_user = db.query(User).filter(User.status ==1)
    
#     check_user_name = get_user.filter(User.first_name == field.first_name).first()
#     if check_user_name:
#         return {"status":0,"msg":"User name already exits."}
    
#     check_email =  get_user.filter(User.email == field.email).first()
#     if check_email:
#         return {"status":0,"msg":"Email already exits."}
    
#     check_mobile =  get_user.filter(User.phone_number == field.phone_number).first()
#     if check_mobile:
#         return {"status":0,"msg":"Mobile number already exits."}
    
    
#     create_user = User(
 
    
#         first_name = field.first_name,
#         last_name = field.last_name,
#         date_of_birth=field.date_of_birth,
#         gender=field.gender,
#         role="student",
#         email = field.email,
#         password=get_password_hash(field.password),
#         phone_number = field.phone_number,
#         blood_group=field.blood_group,
#         mother_tongue=field.mother_tongue,
#         aadhaar_num=field.aadhaar_num,
#         is_hosteller=field.is_hosteller,
#         specially_abled_person=field.specially_abled_person,
#         umis_no=field.umis_no,
#         father_name=field.father_name,
#         mother_name=field.mother_name,
#         parent_phone=field.parent_phone,
#         emergency_num=field.emergency_num,
#         date_of_join=field.date_of_join,
#         address_id=address_add.id,
#         created_by=

#     db.add(create_user)
#     db.commit()
    
#     return {"status":1,"msg":"Now you can enjoy with your credentials keep login"}

@router.post('/login-user')
async def login_user(db:Session=Depends(deps.get_db),Email_or_phone:str=Form(...),Password:str=Form(...),
                    ):
    checkUser = db.query(User).filter(or_(
                                          User.email == Email_or_phone,
                                          User.phone_number == Email_or_phone),
                                      User.status ==1).first()
    
    if not checkUser:
        return {"status":0,"msg":"invalid credentials"}
    password_verification = verify_password(Password,checkUser.password)
    if not password_verification:
        return {"status":0,"msg":"Invalid credentials"}
    else:
        token_deactivate=db.query(Apitoken).filter(Apitoken.user_id==checkUser.id,Apitoken.status==1).first()
        if token_deactivate:
            token_deactivate.status=0
            db.commit()

        char1 = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
        char2 = 'QWERTYUIOPLKJHGFDSAZXCVBNM0123456789'
        reset_character = char1 + char2
        key = ''.join(random.choices(reset_character, k=30))
        
        token =f"{key}{checkUser.id}"
    
        create_token = Apitoken(
            user_id = checkUser.id,
            token = token,
            created_at = datetime.now(),
            status = 1
        )
        db.add(create_token)
        db.commit()
        
        return {"status":1,"msg":"Login successfully","token":token}
    
    

@router.post('/create_admin',description="This Route is for Creating Admin Data")
def admin_user(admin:user_schema.Admin_data,db:Session=Depends(deps.get_db),current_user:User=Depends(create_access_token)):
    if current_user.role=="admin":
            create_admin=User(
                email=admin.email,
                password=get_password_hash(admin.password),
                role="admin",
                created_by=current_user.id,
                modified_by=current_user.id
            )    
            db.add(create_admin)
            db.commit()
            return{"status":1,"msg":"Admin profile Created Sucessfully"}
            
    else:
        return{"status":0,"msg":"You are Not Authorized to Access"}
    
@router.post('/create_staff',description="This Route is for Creating Staff Data")
def staff_user(staff:user_schema.staff_data,db:Session=Depends(get_db),current_user:User=Depends(create_access_token)):
    if current_user.role=="admin":
            create_address=Address(
                current_address=staff.address.current_address,
                current_city=staff.address.current_city,
                current_pincode=staff.address.current_pincode,
                permanent_address=staff.address.permanent_address,
                permanent_city=staff.address.permanent_city,
                permanent_pincode=staff.address.permanent_pincode,
                state=staff.address.state,
                country=staff.address.country,
                created_by=current_user.id,
                modified_by=current_user.id

            )
            db.add(create_address)
            db.commit()
            db.refresh(create_address)
            create_staff=User(
                first_name=staff.first_name,
                last_name=staff.last_name,
                date_of_birth=staff.date_of_birth,
                gender=staff.gender,
                role="staff",
                email=staff.email,
                password=get_password_hash(staff.password),
                phone_number=staff.phone_number,
                blood_group=staff.blood_group,
                aadhaar_num=staff.aadhaar_num,
                emergency_num=staff.emergency_num,
                date_of_join=staff.date_of_join,
                address_id=create_address.id,
                created_by=current_user.id,
                modified_by=current_user.id

            )
            db.add(create_staff)
            db.commit()
            return{"status":1,"msg":"Staff profile Created Sucessfully"}
    else:
         return{"status":0,"msg":"You are Not Authorized to Access"}
    
@router.post('/create_student',description="This Route is for Creating Student Data")
def student_user(student:user_schema.Student_data,db:Session=Depends(get_db),current_user:User=Depends(create_access_token)):
    if current_user.role in ["staff", "admin"]:
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
         return{"status":0,"msg":"You are Not Authorized"}

          
          
    

        
        
    
    
        
        
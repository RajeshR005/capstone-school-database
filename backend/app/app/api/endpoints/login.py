
from typing import Optional
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
from app.schemas import user_schema,login_schema

import random


router = APIRouter(prefix="/Authentication")


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


@router.post('/user_login')
async def login_user(db:Session=Depends(get_db),User_name:str=Form(...),Password:str=Form(...)):
    checkUser = db.query(User).filter(or_(
                                          User.email == User_name,
                                          User.phone_number == User_name),
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
        
        token =f"{key}{checkUser.id}ytrewq"
    
        create_token = Apitoken(
            user_id = checkUser.id,
            token = token,
            created_at = datetime.now(),
            status = 1
        )
        db.add(create_token)
        db.commit()
        user_data={
            "first_name":checkUser.first_name,
            "last_name":checkUser.last_name,
            "email":checkUser.email,
            "User_type":checkUser.role
        }
        
        return {"status":1,"msg":"Login successfully","token":token,"User_data":user_data}
    
@router.post('/validate_token',description="This Route is for Check token")
def validate_token(token:str=Form(...),db:Session=Depends(get_db)):
    check_token=check_token_all(token,db)
    if isinstance(check_token,dict):
        return check_token
    return {"status":1,"msg":"It is Valid Token"}
    
@router.post('/user_logout',description="This Route is for Logout User")
def log_out(token:str=Form(...),db:Session=Depends(get_db)):
    check_token=check_token_all(token,db)
    if isinstance(check_token,dict):
        return check_token
    log_out_status=db.query(Apitoken).filter(Apitoken.user_id==check_token.id,Apitoken.status==1)
    log_out_status.update({Apitoken.status:0})
    db.commit()
    return{"status":1,"msg":f"Log Out Successful {check_token.first_name}"}

@router.post('/change_password',description="This Route is for change password by their own or by admin")
def change_password(token:str=Form(...),old_password:Optional[str]=Form(None),new_password:str=Form(...),confirm_password:str=Form(...),db:Session=Depends(get_db)):
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if get_user.role in ["staff","admin"]:
        change_user_pass=db.query(User).filter(User.email==get_user.email,User.status==1).first()
        check_old_password=verify_password(confirm_password,change_user_pass.password)
        if check_old_password:
            return{"status":0,"msg":"New password couldn't be the old password"}
        if not new_password==confirm_password:
            return{"status":0,"msg":"new Password and confirm password Does not match"}
        change_user_pass.password=get_password_hash(confirm_password)
        db.commit()
        return{"status":1,"msg":f"Your Password Changed Successfully {get_user.email} "}
    else:
        change_user_pass=db.query(User).filter(User.email==get_user.email,User.status==1).first()
        if not old_password:
            return{"status":0,"msg":"Please enter your old Password"}
        check_old_password=verify_password(old_password,change_user_pass.password)
        if not check_old_password:
            return{"status":0,"msg":"The Old Password is Invalid"}
        if old_password==confirm_password:
            return{"status":0,"msg":"New password couldn't be the old password"}
        if not new_password == confirm_password:
            return{"status":0,"msg":"new password and confirm passoword does not match"}
        change_user_pass.password=get_password_hash(confirm_password)
        db.commit()
        return{"status":1,"msg":f"Your password Changed Successfully {get_user.email}"}
    

    

    


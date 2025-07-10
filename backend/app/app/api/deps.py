
from typing import Generator
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
# from app.db.base_class import 
from app.db.session import SessionLocal
from app.core.config import settings
from sqlalchemy.orm import Session
# from fastapi import Depends
from app.models import Apitoken,User,Address
from app.core.security import get_password_hash


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token")

"""Initializing the database Connection"""
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def check_token(token,db:Session):
    check_user_token=db.query(Apitoken).filter(Apitoken.token==token,Apitoken.status==1).first()
    if not check_user_token:
        return{"status":0,"msg":"Invalid Token"}
    get_user=db.query(User).filter(User.id==check_user_token.user_id,User.status==1).first()
    if not get_user:
        return{"status":0,"msg":"No user data found for this token"}
    if get_user.role not in ["admin","staff"]:
        return{"status":0,"msg":"you are not authorized here"}
    return get_user

def check_token_all(token,db:Session):
    check_user_token=db.query(Apitoken).filter(Apitoken.token==token,Apitoken.status==1).first()
    if not check_user_token:
        return{"status":0,"msg":"Invalid Token"}
    get_user=db.query(User).filter(User.id==check_user_token.user_id,User.status==1).first()
    if not get_user:
        return{"status":0,"msg":"No user data found for this token"}
    if get_user.role not in ["admin","staff","student","staff-office","principal"]:
        return{"status":0,"msg":"you are not authorized here"}
    return get_user

def create_user_data(creater:int,field,db:Session):
    create_address=Address(
                current_address=field.address.current_address,
                current_city=field.address.current_city,
                current_pincode=field.address.current_pincode,
                permanent_address=field.address.permanent_address,
                permanent_city=field.address.permanent_city,
                permanent_pincode=field.address.permanent_pincode,
                state=field.address.state,
                country=field.address.country,
                created_by=creater,
                modified_by=creater

            )
    db.add(create_address)
    db.commit()
    db.refresh(create_address)
    create_field=User(
                first_name=field.first_name,
                last_name=field.last_name,
                date_of_birth=field.date_of_birth,
                gender=field.gender,
                email=field.email,
                password=get_password_hash(field.password),
                phone_number=field.phone_number,
                blood_group=field.blood_group,
                mother_tongue=field.mother_tongue,
                aadhaar_num=field.aadhaar_num,
                is_hosteller=field.is_hosteller,
                specially_abled_person=field.specially_abled_person,
                umis_no=field.umis_no,
                father_name=field.father_name,
                mother_name=field.mother_name,
                parent_phone=field.parent_phone,
                emergency_num=field.emergency_num,
                date_of_join=field.date_of_join,
                role=field.user_type,
                address_id=create_address.id,
                created_by=creater,
                modified_by=creater

            )
    db.add(create_field)
    db.commit()
    return{"status":1,"msg":f"profile Created Sucessfully for {field.user_type}"}

def View_data(view_user_data,view_address_data):
    user_data=view_user_data
    Address_data=view_address_data
    return_data={
    "first_name":user_data.first_name,
    "last_name":user_data.last_name,
    "date_of_birth":user_data.date_of_birth,
    "gender":user_data.gender,
    "email":user_data.email,
    "phone_number":user_data.phone_number,
    "blood_group":user_data.blood_group,
    "mother_tongue":user_data.mother_tongue,
    "aadhaar_num":user_data.aadhaar_num,
    "is_hosteller":user_data.is_hosteller,
    "specially_abled_person":user_data.specially_abled_person,
    "umis_no":user_data.umis_no,
    "father_name":user_data.father_name,
    "mother_name":user_data.mother_name,
    "parent_phone":user_data.parent_phone,
    "emergency_num":user_data.emergency_num,
    "date_of_join":user_data.date_of_join,
    "role":user_data.role,
    
    }
    if Address_data:
        return_data["address_data"]={
            "current_address":Address_data.current_address,
            "current_city":Address_data.current_city,
            "current_pincode":Address_data.current_pincode,
            "permanent_address":Address_data.permanent_address,
            "permanent_city":Address_data.permanent_city,
            "permanent_pincode":Address_data.permanent_pincode,
            "state":Address_data.state,
            "country":Address_data.country
        }
    else:
        return_data["address"]=None
    return return_data
    

def count_attendance(attendance_list):
    from collections import Counter
    status_map = {0: "absent", 1: "present", 2: "half_morning", 3: "half_afternoon", 4: "on_duty"}
    status_counter = Counter([a.status for a in attendance_list])
    total = sum(status_counter.values())
    result = {i: status_counter.get(j, 0) for j, i in status_map.items()}
    result["total_days"] = total
    if total > 0:
        for i in ["present"]:
            result["present_percent"] = round((result[i] / total) * 100, 2)
    return result

        

         

                

          

    
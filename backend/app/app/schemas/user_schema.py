from pydantic import BaseModel, EmailStr
from sqlalchemy import Date,Boolean
from datetime import date,time,datetime,timedelta
from typing import Optional






class Admin_data(BaseModel):
    email:EmailStr
    password:str

class Address_add(BaseModel):
    current_address:str
    current_city:str
    current_pincode:str
    permanent_address:str
    permanent_city:str
    permanent_pincode:str
    state:str
    country:str

class staff_data(BaseModel):
    first_name:str
    last_name:str
    date_of_birth:date
    gender:str
    email:EmailStr
    password:str
    phone_number:str
    blood_group:str
    aadhaar_num:str
    emergency_num:str
    date_of_join:date
    
    address:Address_add






class Student_data(BaseModel):
    first_name:str
    last_name:str
    date_of_birth:date
    gender:str
    email:EmailStr
    password:str
    phone_number:str
    blood_group:str
    mother_tongue:str
    aadhaar_num:str
    is_hosteller:bool
    specially_abled_person:bool
    umis_no:str
    father_name:str
    mother_name:str
    parent_phone:str
    emergency_num:str
    date_of_join:date
    
    address:Address_add

#-------------------------------------update-----------------------------
class Address_update(BaseModel):
    current_address:Optional[str]=None
    current_city:Optional[str]=None
    current_pincode:Optional[str]=None
    permanent_address:Optional[str]=None
    permanent_city:Optional[str]=None
    permanent_pincode:Optional[str]=None
    state:Optional[str]=None
    country:Optional[str]=None

class Update_user(BaseModel):
    token:str
    id:Optional[int]=None
    user_type:str
    first_name:Optional[str]=None
    last_name:Optional[str]=None
    date_of_birth:Optional[date]=None
    gender:Optional[str]=None
    email:Optional[EmailStr]=None
    phone_number:Optional[str]=None
    blood_group:Optional[str]=None
    mother_tongue:Optional[str]=None
    aadhaar_num:Optional[str]=None
    is_hosteller:Optional[bool]=None
    specially_abled_person:Optional[bool]=None
    umis_no:Optional[str]=None
    father_name:Optional[str]=None
    mother_name:Optional[str]=None
    parent_phone:Optional[str]=None
    emergency_num:Optional[str]=None
    date_of_join:Optional[date]=None
    
    address:Optional[Address_update]=None



# class Update_staff_and_student(BaseModel):
#     password:Optional[str]=None
#     phone_number:Optional[str]=None
#     aadhaar_num:Optional[str]=None
#     umis_no:Optional[str]=None
#     parent_phone:Optional[str]=None
#     emergency_num:Optional[str]=None
    
#     address:Optional[Address_update]=None

# class Update_student(BaseModel):
#     password:Optional[str]=None
#     phone_number:Optional[str]=None



class Email_in(BaseModel):
    email:EmailStr

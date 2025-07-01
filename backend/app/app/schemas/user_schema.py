from pydantic import BaseModel, EmailStr
from sqlalchemy import Date,Boolean
from datetime import date,time,datetime,timedelta






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

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
from faker import Faker


router = APIRouter()

fake = Faker('en_IN')  



@router.post('/create_bulk_students/{count}', description="Bulk create fake students")
def create_bulk_students(
    count: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(create_access_token)
):
    if current_user.role not in ["staff", "admin"]:
        return{"status":0,"msg":"You are not Authorized Here !"}
    
    created_count = 0
    for i in range(count):
        fake_email = fake.unique.email()
        if db.query(User).filter(User.email == fake_email, User.status == 1).first():
             return{"status":0,"msg":"User already exists"}
           
        address = Address(
            current_address=fake.address(),
            current_city=fake.city(),
            current_pincode=fake.postcode(),
            permanent_address=fake.address(),
            permanent_city=fake.city(),
            permanent_pincode=fake.postcode(),
            state=fake.state(),
            country="India",
            created_by=current_user.id,
            modified_by=current_user.id
        )
        db.add(address)
        db.commit()
        db.refresh(address)

        student = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=10, maximum_age=18),
            gender=fake.random_element(elements=["Male", "Female"]),
            role="student",
            email=fake_email,
            password=get_password_hash("hello@02"),  
            phone_number=fake.phone_number(),
            blood_group=fake.random_element(elements=["A+", "B+", "O+", "AB+"]),
            mother_tongue=fake.random_element(elements=["Tamil", "Hindi", "English"]),
            aadhaar_num=fake.random_number(digits=12, fix_len=True),
            is_hosteller=fake.boolean(),
            specially_abled_person=fake.boolean(),
            umis_no=fake.random_int(min=100000, max=999999),
            father_name=fake.name_male(),
            mother_name=fake.name_female(),
            parent_phone=fake.phone_number(),
            emergency_num=fake.phone_number(),
            date_of_join=fake.date_this_decade(),
            address_id=address.id,
            created_by=current_user.id,
            modified_by=current_user.id
        )
        db.add(student)
        created_count += 1

    db.commit()
    return {"status": 1, "msg": f"{created_count} student profiles created successfully."}




@router.post('/create_bulk_staffs/{count}', description="Bulk create fake students")
def create_bulk_staffs(count: int,db: Session = Depends(get_db),current_user: User = Depends(create_access_token)):
    if current_user.role not in ["staff", "admin"]:
        return{"status":0,"msg":"You are not authorized Here "}
    
    created_count = 0
    for i in range(count):
        fake_email = fake.unique.email()
        if db.query(User).filter(User.email == fake_email, User.status == 1).first():
             return{"status":0,"msg":"User already exists"}
           
        address = Address(
            current_address=fake.address(),
            current_city=fake.city(),
            current_pincode=fake.postcode(),
            permanent_address=fake.address(),
            permanent_city=fake.city(),
            permanent_pincode=fake.postcode(),
            state=fake.state(),
            country="India",
            created_by=current_user.id,
            modified_by=current_user.id
        )
        db.add(address)
        db.commit()
        db.refresh(address)

        student = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=25, maximum_age=45),
            gender=fake.random_element(elements=["Male", "Female"]),
            role="staff",
            email=fake_email,
            password=get_password_hash("staff@02"),  
            phone_number=fake.phone_number(),
            blood_group=fake.random_element(elements=["A+", "B+", "O+", "AB+"]),
            mother_tongue=fake.random_element(elements=["Tamil", "Hindi", "English"]),
            aadhaar_num=fake.random_number(digits=12, fix_len=True),
            emergency_num=fake.phone_number(),
            date_of_join=fake.date_this_decade(),
            address_id=address.id,
            created_by=current_user.id,
            modified_by=current_user.id
        )
        db.add(student)
        created_count += 1

    db.commit()
    return {"status": 1, "msg": f"{created_count} staff profiles created successfully."}


        
        
    
    
        
           
        
    
    
        
        
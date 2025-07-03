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


router = APIRouter(prefix="/user")

@router.post('/edit_user/',description="This Route is for Updating the User's Details")
def Edit_user(field:user_schema.Update_user,db:Session=Depends(get_db)):
    check_token=db.query(Apitoken).filter(Apitoken.token==field.token,Apitoken.status==1).first()
    if not check_token:
        return{"status":0,"msg":"Invalid Token"}
    get_current_user=db.query(User).filter(User.id==check_token.user_id,User.status==1)
    staff_instance=get_current_user.first()
    if not staff_instance:
        return{"status":0,"msg":"No user Data Found for this token"}
    if staff_instance.role not in ["staff","admin"]:
        return{"status":0,"msg":"You are Not Authorized Here !"}
    if staff_instance.role in ["staff"]:
        if field.user_type=="staff":
            if staff_instance.id!=field.id:
               return{"status":0,"msg":"You can't edit other Staff's Data"}
            update_data=field.model_dump(exclude_unset=True)
            update_data.pop("address",None)
            update_data.pop("user_type")
            update_data.pop("token")
            get_current_user.update(update_data,synchronize_session=False)
            if field.address:
                get_address=db.query(Address).filter(Address.id==staff_instance.address_id,Address.status==1).first()
                if get_address:
                    new_address=field.address.model_dump(exclude_unset=True)
                    for key,value in new_address.items():
                        setattr(get_address,key,value)
            get_current_user.modified_by=staff_instance.id
            db.commit()
            return{"status":1,"msg":f"Your Data Updated Sucessfully"}
        elif field.user_type=="student":
            student_data=db.query(User).filter(User.id==field.id,User.role=="student",User.status==1)
            student_instance=student_data.first()
            if not student_instance:
                return{"status":0,"msg":"No Student Data Found with this ID"}
            update_student=field.model_dump(exclude_unset=True)
            update_student.pop("address",None)
            update_student.pop("user_type")
            update_student.pop("token")
            student_data.update(update_student,synchronize_session=False)
            if field.address:
                get_address=db.query(Address).filter(Address.id==student_instance.address_id,Address.status==1).first()
                if get_address:
                    new_address=field.address.model_dump(exclude_unset=True)
                    for key,value in new_address.items():
                        setattr(get_address,key,value)
            student_instance.modified_by=staff_instance.id
            db.commit()
            return{"status":0,"msg":"Student Data Updated Successfully"}
    elif staff_instance.role in ["admin"]:
        if field.user_type=="student":
            update_data=db.query(User).filter(User.id==field.id,User.role=="student",User.status==1)
            update_instance=update_data.first()
            
            if not update_instance:
                return{"status":0,"msg":"No Student Data Found "}
            update_user=field.model_dump(exclude_unset=True)
            update_user.pop("address",None)
            update_user.pop("user_type")
            update_user.pop("token")
            update_data.update(update_user,synchronize_session=False)
            if field.address:
                get_address=db.query(Address).filter(Address.id==update_instance.address_id,Address.status==1).first()
                if get_address:
                    new_address=field.address.model_dump(exclude_unset=True)
                    for key,value in new_address.items():
                        setattr(get_address,key,value)
            update_instance.modified_by=staff_instance.id
            db.commit()
            return{"status":1,"msg":"Student Data Updated Successfully"}
        
        elif field.user_type=="staff":
    
            update_data=db.query(User).filter(User.id==field.id,User.role=="staff",User.status==1)
            update_instance=update_data.first()
            
            if not update_instance:
                return{"status":0,"msg":"No Staff Data Found "}
            update_user=field.model_dump(exclude_unset=True)
            update_user.pop("address",None)
            update_user.pop("user_type")
            update_user.pop("token")
            update_data.update(update_user,synchronize_session=False)
            if field.address:
                get_address=db.query(Address).filter(Address.id==update_instance.address_id,Address.status==1).first()
                if get_address:
                    new_address=field.address.model_dump(exclude_unset=True)
                    for key,value in new_address.items():
                        setattr(get_address,key,value)
            update_instance.modified_by=staff_instance.id
            db.commit()
            return{"status":1,"msg":"Staff Data Updated Successfully"}
        elif field.user_type=="admin":
            update_data=db.query(User).filter(User.id==field.id,User.role=="admin",User.status==1)
            update_instance=update_data.first()
            
            if not update_instance:
                return{"status":0,"msg":"No Admin Data Found "}
            update_user=field.model_dump(exclude_unset=True)
            update_user.pop("address",None)
            update_user.pop("user_type")
            update_user.pop("token")
            update_data.update(update_user,synchronize_session=False)
            if field.address:
                get_address=db.query(Address).filter(Address.id==update_instance.address_id,Address.status==1).first()
                if get_address:
                    new_address=field.address.model_dump(exclude_unset=True)
                    for key,value in new_address.items():
                        setattr(get_address,key,value)
            update_instance.modified_by=staff_instance.id
            db.commit()
            return{"status":1,"msg":"Admin Data Updated Successfully"}
        

    
        

            

# @router.post('/update_data_by_staff/{email},{user_type}',description="This Route is for Updating the Staff Details By staff(own)")
# def update_data_by_staff(email:EmailStr,user_type:str,field:user_schema.Update_staff_and_student,db:Session=Depends(get_db),current_user:User=Depends(create_access_token)):
#     if current_user.role!="staff":
#         return{"status":0,"msg":"You are not Authorized Here !"}
#     if user_type=="staff":
#         update_user=db.query(User).filter(User.email==email,User.role=="staff",User.id==current_user.id,User.status==1)
#         user_instance=update_user.first()
#         if not user_instance:
#             return{"status":0,"msg":f"No User Data Found with this Email: {email} !"}
#         # print("user_instance.address_id:", user_instance.address_id)
#         update_data=field.model_dump(exclude_unset=True)
#         update_data.pop("address",None)
#         if field.password:
#             update_data["password"]=get_password_hash(update_data["password"])
#         update_user.update(update_data,synchronize_session=False)
#         if field.address:
#             get_address=db.query(Address).filter(Address.id==user_instance.address_id,Address.status==1).first()
#             if get_address:
#                 new_address=field.address.model_dump(exclude_unset=True)
#                 for key,value in new_address.items():
#                     setattr(get_address,key,value)

#         db.commit()
#         return{"status":1,"msg":"Your Data Updated Sucessfully"}
#     elif user_type=="student":
#         update_user=db.query(User).filter(User.email==email,User.role=="student",User.status==1)
#         user_instance=update_user.first()
#         if not user_instance:
#             return{"status":0,"msg":f"No User Data Found with this Email: {email} !"}
#         # print("user_instance.address_id:", user_instance.address_id)
#         update_data=field.model_dump(exclude_unset=True)
#         update_data.pop("address",None)
#         if field.password:
#             update_data["password"]=get_password_hash(update_data["password"])
#         update_user.update(update_data,synchronize_session=False)
#         if field.address:
#             get_address=db.query(Address).filter(Address.id==user_instance.address_id,Address.status==1).first()
#             if get_address:
#                 new_address=field.address.model_dump(exclude_unset=True)
#                 for key,value in new_address.items():
#                     setattr(get_address,key,value)

#         db.commit()
#         return{"status":1,"msg":"Student Data Updated Sucessfully"}
#     else:
#         return{"status":0,"msg":"The user Type is not Valid"}

# @router.post('/update_data_by_student/{email}',description="This Route is for Updating the User's Details By Admin")
# def update_data_by_student(email:EmailStr,field:user_schema.Update_student,db:Session=Depends(get_db),current_user:User=Depends(create_access_token)):
#     if current_user.role!="student":
#         return{"status":0,"msg":"You are not Authorized Here !"}
#     update_user=db.query(User).filter(User.email==email,User.id==current_user.id,User.status==1)
#     user_instance=update_user.first()
    

#     if not user_instance:
#         return{"status":0,"msg":f"You cannot update other User's Data {email} !"}
#     # print("user_instance.address_id:", user_instance.address_id)
#     update_data=field.model_dump(exclude_unset=True)
#     if field.password:
#         update_data["password"]=get_password_hash(update_data["password"])
#     update_user.update(update_data,synchronize_session=False)

#     db.commit()
#     return{"status":1,"msg":"Your Data Updated Sucessfully"}

    
    
    
    

    

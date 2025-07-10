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
from sqlalchemy.exc import SQLAlchemyError


import random
#---------------------------------------------ADD--------------------------------------------------------------------------------------
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

#-------------------------------------------------Update-----------------------------------------------------------------------------------
        
        # elif field.user_type=="staff":
    
        #     update_data=db.query(User).filter(User.id==field.id,User.role=="staff",User.status==1)
        #     update_instance=update_data.first()
            
        #     if not update_instance:
        #         return{"status":0,"msg":"No Staff Data Found "}
        #     update_user=field.model_dump(exclude_unset=True)
        #     update_user.pop("address",None)
        #     update_user.pop("user_type")
        #     update_user.pop("token")
        #     update_data.update(update_user,synchronize_session=False)
        #     if field.address:
        #         get_address=db.query(Address).filter(Address.id==update_instance.address_id,Address.status==1).first()
        #         if get_address:
        #             new_address=field.address.model_dump(exclude_unset=True)
        #             for key,value in new_address.items():
        #                 setattr(get_address,key,value)
        #     update_instance.modified_by=staff_instance.id
        #     db.commit()
        #     return{"status":1,"msg":"Staff Data Updated Successfully"}
        # elif field.user_type=="admin":
        #     update_data=db.query(User).filter(User.id==field.id,User.role=="admin",User.status==1)
        #     update_instance=update_data.first()
            
        #     if not update_instance:
        #         return{"status":0,"msg":"No Admin Data Found "}
        #     update_user=field.model_dump(exclude_unset=True)
        #     update_user.pop("address",None)
        #     update_user.pop("user_type")
        #     update_user.pop("token")
        #     update_data.update(update_user,synchronize_session=False)
        #     if field.address:
        #         get_address=db.query(Address).filter(Address.id==update_instance.address_id,Address.status==1).first()
        #         if get_address:
        #             new_address=field.address.model_dump(exclude_unset=True)
        #             for key,value in new_address.items():
        #                 setattr(get_address,key,value)
        #     update_instance.modified_by=staff_instance.id
        #     db.commit()
        #     return{"status":1,"msg":"Admin Data Updated Successfully"}
        

    
        

            

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

    
    
    
    

    

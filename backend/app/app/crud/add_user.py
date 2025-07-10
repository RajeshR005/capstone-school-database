from typing import Optional
from fastapi import APIRouter, Depends, Form,requests
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import get_db,check_token,create_user_data,View_data,check_token_all
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_

from app.schemas import user_schema,login_schema
from sqlalchemy.exc import SQLAlchemyError


import random

router = APIRouter(prefix="/user")




@router.post('/add_user',description="This Route is for Add User Accessed by Only Admin and Staff")
def add_user(field:user_schema.Student_data,db:Session=Depends(get_db)):
    get_user=check_token(field.token,db)
    if isinstance(get_user,dict):
        return get_user
    check_duplicate=db.query(User).filter(User.email==field.email,User.status==1).first()
    if check_duplicate:
                  return{"status":0,"msg":"User Data Already Exists"}
    creater=get_user.id
    new_data=create_user_data(creater,field,db)
    return new_data


@router.post('/edit_user',description="This Route is for Updating the User's Details "
"If Admin only Required is Id and Token, If Staff by their own Data they Need User_type only If they need to Update student Data They need Id along with User's Type")
def Edit_user(field:user_schema.Update_user,db:Session=Depends(get_db)):
    get_user=check_token(field.token,db)
    if isinstance(get_user,dict):
        return get_user
    exist_user=db.query(User).filter(User.email==field.email,User.status==1)
    user_instance=exist_user.first()
    try:
        if get_user.role=="staff":
            if field.user_type=="staff":
                if user_instance.role!="staff":
                    return{"status":"This user is not a staff"}
                if get_user.email!=field.email:
                   return{"status":0,"msg":"You can't edit other Staff's Data"}
                update_data=field.model_dump(exclude_unset=True)
                update_data.pop("address",None)
                update_data.pop("user_type",None)
                update_data.pop("token",None)
                exist_user.update(update_data,synchronize_session=False)
                if field.address:
                    get_address=db.query(Address).filter(Address.id==get_user.address_id,Address.status==1).first()
                    if get_address:
                        new_address=field.address.model_dump(exclude_unset=True)
                        for key,value in new_address.items():
                            setattr(get_address,key,value)
                exist_user.modified_by=get_user.id
                db.commit()
                return{"status":1,"msg":f"Your Data Updated Sucessfully"}
            elif field.user_type=="student":
                student_data=db.query(User).filter(User.email==field.email,User.role=="student",User.status==1)
                student_instance=student_data.first()
                if not student_instance:
                    return{"status":0,"msg":"No Student Data Found with this ID"}
                update_student=field.model_dump(exclude_unset=True)
                update_student.pop("address",None)
                update_student.pop("user_type",None)
                update_student.pop("token",None)
                student_data.update(update_student,synchronize_session=False)
                if field.address:
                    get_address=db.query(Address).filter(Address.id==student_instance.address_id,Address.status==1).first()
                    if get_address:
                        new_address=field.address.model_dump(exclude_unset=True)
                        for key,value in new_address.items():
                            setattr(get_address,key,value)
                student_instance.modified_by=get_user.id
                db.commit()
                return{"status":1,"msg":"Student Data Updated Successfully"}
        elif get_user.role in ["admin"]:
            update_data=db.query(User).filter(User.email==field.email,User.status==1)
            update_instance=update_data.first()
            
            if not update_instance:
                return{"status":0,"msg":"No User Data Found "}
            
            update_user=field.model_dump(exclude_unset=True)
            update_user.pop("address",None)
            update_user.pop("user_type",None)
            update_user.pop("token",None)
            if not update_user and not field.address:
                return {"status": 0, "msg": "No update data provided."}

            update_data.update(update_user,synchronize_session=False)
            if field.address:
                get_address=db.query(Address).filter(Address.id==update_instance.address_id,Address.status==1).first()
                if not get_address:
                    return{"status":0,"msg":"No Address Id found for this user"}
                new_address=field.address.model_dump(exclude_unset=True)
                for key,value in new_address.items():
                    setattr(get_address,key,value)
            update_instance.modified_by=get_user.id
            db.commit()
            return{"status":1,"msg":"User Data Updated Successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return{"status":0,"msg":f"An SQLAlchemyError {e}"}
    except Exception as e:
        db.rollback()
        return{"status":0,"msg":f"An Error Occured {e}"}    
    
@router.post('/view_user',description="This Route is used to view the details of their own data or by Admin")
def view_user(token:str=Form(...),User_name:Optional[str]=Form(None),db:Session=Depends(get_db)):
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if get_user.role=="admin":
        view_user_data=db.query(User).filter(User.email==User_name,User.status==1).first()
        # print(view_user_data)
        if not view_user_data:
            return{"status":0,"msg":"No User data found"}
        view_address_data=db.query(Address).filter(Address.id==view_user_data.address_id).first()
        
        return View_data(view_user_data,view_address_data)
    else:
        view_user_data=db.query(User).filter(User.id==get_user.id,User.status==1).first()
        if not view_user_data:
            return{"status":0,"msg":"No User data found"}
        view_address_data=db.query(Address).filter(Address.id==view_user_data.address_id).first()
        return View_data(view_user_data,view_address_data)   

@router.post('/delete_user',description="This Router is for Delete User Data Accessed by Only Admin")
def delete_user(token:str=Form(...),email:EmailStr=Form(...),change_status:int=Form(...),db:Session=Depends(get_db)):
    auth_user=check_token(token,db)
    if not auth_user.role=="admin":
        return{"status":0,"msg":"You are not authorized to delete User's data"}
    delete_user=db.query(User).filter(User.email==email)
    delete_user_instance=delete_user.first()
    if not delete_user_instance:
        return{"status":0,"msg":"No user data found"}
    delete_user.update({User.status:change_status})
    db.commit()
    if change_status==1:
        return{"status":0,"msg":f"User Data with {email} Activated Successfully"}
    elif change_status==-1:
        return{"staus":0,"msg":f"User Data with {email} In-Activated Successfully"}
    elif change_status==0:
        return{"status":0,"msg":f"User Data with {email} Deleted Successfully"}
    else:
        return{"status":0,"msg":"Invalid Status id"}
    

        



@router.post('/list_users',description="This Route is used for View User's Data by Admin Only")
def list_users(page_no:int=Form(...),limit_no:int=Form(...),token:str=Form(...),db:Session=Depends(get_db)):
    get_users=check_token(token,db)
    if isinstance(get_users,dict):
        return get_users
    if not get_users.role=="admin":
        return{"status":0,"msg":"You are not authorized here"}
    
    get_total_count = db.query(User).filter(User.status == 1).count()
    if not get_total_count:
        return{"status":0,"msg":"No Data Available"}
    total_page, offset, limit = get_pagination(get_total_count, page_no, limit_no)

    get_users = db.query(User).filter(User.status == 1).offset(offset).limit(limit).all()
    
    final_list=[]
    for user_data in get_users:
        get_address=db.query(Address).filter(Address.id==user_data.address_id,User.status==1).first()
        if get_address is None:
            get_address=None
        user_list=View_data(user_data,get_address)
        final_list.append(user_list)

    return paginate(page_no, limit_no, final_list, total_page, get_total_count)






    


          
          





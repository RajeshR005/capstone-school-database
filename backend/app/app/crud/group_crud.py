from fastapi import APIRouter, Depends, Form,requests
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import get_db,check_token_all,check_token
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from app.schemas import user_schema,login_schema,attendance_schema
from typing import Optional
router=APIRouter()

@router.post('/add_groups',description="This Route is for Adding Data in the Group table")
def add_groups(token:str=Form(...),group_name:str=Form(...),group_description:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_grp=db.query(Group).filter(Group.group_name==group_name.capitalize(),Group.status==1).first()
    if get_grp:
        return{"status":0,"msg":f"The {group_name} Already exists in the Database "}
    grp_up=group_name.capitalize()
    add_grp=Group(
        group_name=grp_up,
        description=group_description,
        created_by=get_admin.id,
        modified_by=get_admin.id
    )
    db.add(add_grp)
    db.commit()
    return{"status":1,"msg":f"{grp_up} Added Successfully in the Database"}

@router.post('/edit_groups',description="This Route is for Editing the Data of the Groups in the Database ")
def edit_groups(token:str=Form(...),Group_id:int=Form(...),modify_group_name:Optional[str]=Form(None),modify_description:Optional[str]=Form(None),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_grp=db.query(Group).filter(Group.id==Group_id,Group.status==1)
    get_grp_instance=get_grp.first()
    if not get_grp_instance:
        return{"status":0,"msg":f"There is no Data available for this Group id: {Group_id}"}
    if modify_group_name =="string" and modify_description =="string":
        return{"status":0,"msg":"There is no data provided for the update"}
    if modify_group_name:
        get_grp_instance.group_name=modify_group_name
    if modify_description:
        get_grp_instance.description=modify_description
    db.commit()
    return {"status":1,"msg":f"Data Updated Successfully for the Group ID {Group_id}"}

@router.post('/list_groups_data_active',description="This Route is used to View the Active Group's Data in the DB")
def list_groups_data_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_grp=db.query(Group).filter(Group.status==1).all()
    if not view_grp:
        return{"status":0,"msg":"No Active Group Data Available in the DB"}
    return view_grp

@router.post('/list_groups_data_in_active',description="This Route is used to View the In-Active Group's Data in the DB")
def list_groups_data_in_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_grp=db.query(Group).filter(Group.status==-1).all()
    if not view_grp:
        return{"status":0,"msg":"No In-active Group Data Available in the DB"}
    return view_grp

@router.post('/change_status_groups',description="This Route is for change status of  Data in the Group's table")
def change_status_groups(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_grp=db.query(Group).filter(Group.id==id).first()
    if not change_status_grp:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_grp.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_grp.id} Activated Sucessful"}
    elif change_status==2:
        return{"status":1,"msg":f"{change_status_grp.id} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_grp.id} In-Activated Sucessful"}
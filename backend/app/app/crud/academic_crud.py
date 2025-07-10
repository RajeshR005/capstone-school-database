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

@router.post('/add_academic_years',description="This Route is for Adding Data in the Academic year table")
def add_academic_year(token:str=Form(...),Academic_Year_data:str=Form(...),start_date:date=Form(...),end_date:date=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_acad=db.query(AcademicYear).filter(AcademicYear.academic_year==Academic_Year_data,AcademicYear.status==1).first()
    if get_acad:
        return{"status":0,"msg":f"The {Academic_Year_data}  Already exists in the Database "}
    if start_date>=end_date:
        return{"status":0,"msg":"The End Data should be greater than Start Date"}
    add_acad=AcademicYear(
        academic_year=Academic_Year_data,
        start_date=start_date,
        end_date=end_date,
        created_by=get_admin.id,
        modified_by=get_admin.id
    )
    db.add(add_acad)
    db.commit()
    return{"status":1,"msg":f"{Academic_Year_data} Added Successfully in the Database"}

@router.post('/edit_academic_year_data',description="This Route is for Editing the Data of the Academic table in the Database ")
def edit_academic_year(token:str=Form(...),academic_year_id:int=Form(...),modify_start_date:Optional[date]=Form(None),modify_end_date:Optional[date]=Form(None),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    get_acad=db.query(AcademicYear).filter(AcademicYear.id==academic_year_id,AcademicYear.status==1)
    get_acad_instance=get_acad.first()
    if not get_acad_instance:
        return{"status":0,"msg":f"There is no Data available for this : {academic_year_id}"}
    if modify_start_date is None and modify_end_date is None:
        return{"status":0,"msg":"There is no data provided for the update"}
    if modify_start_date>=modify_end_date:
        return{"status":0,"msg":"The End Data should be greater than Start Date"}
    if modify_start_date:
        get_acad_instance.start_date=modify_start_date
    if modify_end_date:
        get_acad_instance.end_date=modify_end_date
    db.commit()
    return {"status":1,"msg":f"Data Updated Successfully for the Academic Year ID {academic_year_id}"}

@router.post('/list_academic_data_active',description="This Route is used to View the Academic Data which is Active in the DB")
def list_academic_data_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_acad=db.query(AcademicYear).filter(AcademicYear.status==1).all()
    if not view_acad:
        return{"status":0,"msg":"No Active Academic Data Available in the DB"}
    return view_acad

@router.post('/list_academic_data_in_active',description="This Route is used to View the Academic Data which is In-Active in the DB")
def list_academic_data_in_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    view_acad=db.query(AcademicYear).filter(AcademicYear.status==-1).all()
    if not view_acad:
        return{"status":0,"msg":"No In-Active Academic Data Available in the DB"}
    return view_acad

@router.post('/change_status_Academic_year',description="This Route is for change status of  Data in the Academic table")
def change_status_Academic_year(token:str=Form(...),id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_admin=check_token(token,db)
    if isinstance(get_admin,dict):
        return get_admin
    if get_admin.role!="admin":
        return{"status":0,"msg":"You are not Authorized here"}
    change_status_acad=db.query(AcademicYear).filter(AcademicYear.id==id).first()
    if not change_status_acad:
        return{"status":0,"msg":"No Data Found"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    change_status_acad.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{change_status_acad.id} Activated Sucessful"}
    elif change_status==2:
        return{"status":1,"msg":f"{change_status_acad.id} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{change_status_acad.id} In-Activated Sucessful"}
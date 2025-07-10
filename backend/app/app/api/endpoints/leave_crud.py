from fastapi import APIRouter, Depends, File, Form, UploadFile,requests
from fastapi.responses import FileResponse
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import get_db,check_token_all,count_attendance
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from app.schemas import user_schema,login_schema,attendance_schema
from typing import Optional
from pathlib import Path

router=APIRouter(prefix="/leave")

@router.post('/add_leave_request',description="This Route is for Adding the Leave Request by Staffs and Students")
def add_leave_request(token:str=Form(...),from_date:date=Form(...),to_date:date=Form(...),reason:str=Form(...),db:Session=Depends(get_db)):
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if get_user.role not in ["staff","staff-office","student"]:
        return{"status":0,"msg":"Your are not allowed to submit leave Request"}
    exist_leave_record=db.query(Leave).filter(Leave.user_id==get_user.id,Leave.from_date==from_date,Leave.to_date==to_date).first()
    if exist_leave_record:
        return{'status':0,"msg":"This Leave Request Already Exist you can update that Request"}
    if not from_date>=to_date:
        return{"status":0,"msg":"The From data must be greater that to date"}

    new_record=Leave(
        user_id=get_user.id,
        from_date=from_date,
        to_date=to_date,
        reason=reason,
        created_by=get_user.id,
        modified_by=get_user.id

    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return{"status":1,"msg":f"Attendance Added Successfully","leave_request_id":f"{new_record.leave_id}"}
    
@router.post('/edit_leave_request',description="This Route is for Editing the Existing Leave request")
def edit_leave_request(token:str=Form(...),Existing_leave_id:int=Form(...),from_date:Optional[date]=Form(None),to_date:Optional[date]=Form(None),reason:Optional[str]=Form(None),db:Session=Depends(get_db)):
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if get_user.role not in ["staff","staff-office","student"]:
        return{"status":0,"msg":"Your are not allowed to Edit leave Request"}
    Exist_leave_request=db.query(Leave).filter(Leave.user_id==get_user.id,Leave.leave_id==Existing_leave_id).first()
    if not Exist_leave_request:
        return{"status":0,"msg":"No Leave Request Data Found with your data"}
    if from_date:
        Exist_leave_request.from_date=from_date
    if to_date:
        Exist_leave_request.to_date=to_date
    if reason:
        Exist_leave_request.reason=reason
    db.commit()
    return{"status":0,"msg":"Your Leave Request Updated Successfully","Reference_id":f"{Exist_leave_request.leave_id}"}




def filter_leave_by_date(query, from_date: Optional[date], to_date: Optional[date]):
    if from_date:
        query = query.filter(Leave.from_date >= from_date)
    if to_date:
        query = query.filter(Leave.to_date <= to_date)
    return query


@router.post("/view_leave_request", description="View Leave Requests for students or staffs")
def view_leave_request(field: attendance_schema.ViewAttendance,db: Session = Depends(get_db)):
    get_user = check_token_all(field.token, db)
    if isinstance(get_user, dict):
        return get_user

    from_date = field.from_date
    to_date = field.to_date

    if field.user_type == "student":
        if get_user.role in ["staff", "staff-office"]:
            classroom = db.query(Classroom).filter(Classroom.class_advisor_id == get_user.id, Classroom.status == 1).first()
            if not classroom:
                return {"status": 0, "msg": "No class assigned to this staff"}

            assoc = db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.classroom_id == classroom.id, ClassAcademicAssociation.status == 1).first()
            students = db.query(StudentClass).filter(StudentClass.class_academic_id == assoc.id, StudentClass.status == 1).all()

            data = []
            for stu in students:
                leaves = db.query(Leave).filter(Leave.user_id == stu.student_id)
                leaves = filter_leave_by_date(leaves, from_date, to_date).all()
                student = db.query(User).filter(User.id == stu.student_id).first()

                leave_req_final = []
                for i in leaves:
                    day_count = (i.to_date - i.from_date).days + 1
                    leave_req_final.append({
                        "leave_id": i.leave_id,
                        "from_date": i.from_date,
                        "to_date": i.to_date,
                        "reason": i.reason,
                        "total_days": day_count
                    })
                data.append({
                    "student_id": stu.student_id,
                    "student_name": f"{student.first_name} {student.last_name}",
                    "roll_number": stu.roll_number,
                    "leave_requests": leave_req_final
                })
            return {"status": 1, "msg": "Class Students Leave Requests Fetched", "data": data}

        elif get_user.role == "student":
            leaves = db.query(Leave).filter(Leave.user_id == get_user.id)
            leaves = filter_leave_by_date(leaves, from_date, to_date).all()
            data = []
            for i in leaves:
                data.append({
                    "leave_id": i.leave_id,
                    "from_date": i.from_date,
                    "to_date": i.to_date,
                    "reason": i.reason,
                    "total_days": (i.to_date - i.from_date).days + 1
                })
            return {"status": 1, "msg": "Your Leave Requests", "student_id": get_user.id, "student_name": get_user.first_name + " " + get_user.last_name, "data": data}

    elif field.user_type == "staff":
        if get_user.role in ["staff", "staff-office"]:
            leaves = db.query(Leave).filter(Leave.user_id == get_user.id)
            leaves = filter_leave_by_date(leaves, from_date, to_date).all()
            data = []
            for i in leaves:
                data.append({
                    "leave_id": i.leave_id,
                    "from_date": i.from_date,
                    "to_date": i.to_date,
                    "reason": i.reason,
                    "total_days": (i.to_date - i.from_date).days + 1
                })
            return {"status": 1, "msg": "Your Leave Requests", "staff_id": get_user.id, "staff_name": get_user.first_name + " " + get_user.last_name, "data": data}

        elif get_user.role == "principal":
            staffs = db.query(User).filter(User.role == "staff", User.status == 1).all()
            result = []
            for s in staffs:
                leaves = db.query(Leave).filter(Leave.user_id == s.id)
                leaves = filter_leave_by_date(leaves, from_date, to_date).all()
                leave_req_final = []
                for i in leaves:
                    leave_req_final.append({
                        "leave_id": i.leave_id,
                        "from_date": i.from_date,
                        "to_date": i.to_date,
                        "reason": i.reason,
                        "total_days": (i.to_date - i.from_date).days + 1
                    })
                result.append({
                    "staff_id": s.id,
                    "staff_name": s.first_name + " " + s.last_name,
                    "leave_requests": leave_req_final
                })
            return {"status": 1, "msg": "All Staff Leave Requests", "data": result}

    return {"status": 0, "msg": "Invalid user role or user_type"}


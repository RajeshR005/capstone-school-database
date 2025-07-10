from fastapi import APIRouter, Depends, Form,requests
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

router=APIRouter(prefix="/attendance")

@router.post("/add_attendance_data",description="The Staffs can Add their Student Attendance for their own class using students roll number\n A specific staff can Add the staff Attendance")
def add_attendance_data(field:attendance_schema.AttendanceData,db:Session=Depends(get_db)):
    get_user=check_token_all(field.token,db)
    if isinstance(get_user,dict):
        return get_user
    if  get_user.role not in["staff","staff-office"]:
        return{"status":0,"msg":"Only Staff's can add attendance data"}
    if field.user_type=="student":
        get_staff_cls=db.query(Classroom).filter(Classroom.class_advisor_id==get_user.id,Classroom.status==1).first()
        if not get_staff_cls:
            return{"status":0,"msg":"No Class is Associate with the Staff Id"}
        get_cls_acad_id=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.classroom_id==get_staff_cls.id,ClassAcademicAssociation.status==1).first()
        get_students=db.query(StudentClass).filter(StudentClass.class_academic_id==get_cls_acad_id.id,StudentClass.status==1).all()
        if not get_students:
            return{"status":0,"msg":"No student data available for this class"}
        valid_stu=[]
        for i in get_students:
            valid_stu.append(i.roll_number)
            
        # print (valid_stu)
        get_existing_atten = db.query(Attendance).filter(Attendance.attendance_date == field.Attendance_date).all()
        existing_entries = set((i.user_id, i.attendance_date) for i in get_existing_atten)

        attendance_users=[(field.present_id,1),(field.Absent_id,0),(field.Half_morning,2),(field.Half_afternoon,3),(field.On_duty,4)]
        final_attendance=[]
        not_inserted=[]
        already_inserted=[]
        added_roll=[]
        for user_ids, status in attendance_users:
            if user_ids:
                for roll in user_ids:
                    if roll not in valid_stu:
                        not_inserted.append(roll)
                        continue

                    matched_student = next((s for s in get_students if s.roll_number == roll), None)
                    if not matched_student:
                        not_inserted.append(roll)
                        continue
                    if (matched_student.student_id, field.Attendance_date) in existing_entries:
                        already_inserted.append(roll)
                        continue
                    attendance_entry = Attendance(
                    user_id=matched_student.student_id,
                    attendance_date=field.Attendance_date,
                    status=status,
                    created_by=get_user.id,
                    modified_by=get_user.id
                    )
                    final_attendance.append(attendance_entry)
                    added_roll.append(roll)
                    


        print("Added Roll Numbers:", added_roll)
        print("Valid Roll Numbers:", valid_stu)
        
        db.add_all(final_attendance)
        db.commit()
        return{"status":1,"msg":f"Attendance Data Added Successfully for the students {added_roll}","msg2":f"{not_inserted} These roll no are not in your class","msg3":f"These Attendance Data Already Noted {already_inserted}"}
    elif field.user_type == "staff":
        get_staff = db.query(User).filter(User.role == field.user_type, User.status == 1).all()
        valid_staff = [i.id for i in get_staff]

        get_existing_atten = db.query(Attendance).filter(Attendance.attendance_date == field.Attendance_date).all()
        get_exist_data = [i.user_id for i in get_existing_atten]

        attendance_users = [
            (field.present_id, 1),
            (field.Absent_id, 0),
            (field.Half_morning, 2),
            (field.Half_afternoon, 3),
            (field.On_duty, 4)
        ]

        already_inserted = []
        not_inserted = []
        added_staff = []
        final_attendance = []

        for user_ids, status in attendance_users:
            if user_ids:
                for staff_id in user_ids:
                    if staff_id in get_exist_data:
                        already_inserted.append(staff_id)
                        continue

                    if staff_id not in valid_staff:
                        not_inserted.append(staff_id)
                        continue

                    attendance_entry = Attendance(
                        user_id=staff_id,
                        attendance_date=field.Attendance_date,
                        status=status,
                        created_by=get_user.id,
                        modified_by=get_user.id
                    )
                    final_attendance.append(attendance_entry)
                    added_staff.append(staff_id)

        db.add_all(final_attendance)
        db.commit()
        return {"status": 1,"msg": f"Attendance Data Added Successfully for the staffs {added_staff}","msg2": f"{not_inserted} These Staffs ID's are not available in the DB","msg3": f"These Attendance Data Already Noted {already_inserted}"}

@router.post("/edit_attendance_data", description="Edit attendance of students and Staff by class staff and office staff for a specific date")
def edit_attendance_data(field: attendance_schema.AttendanceData, db: Session = Depends(get_db)):
    get_user = check_token_all(field.token, db)
    if isinstance(get_user, dict):
        return get_user
    if get_user.role not in["staff","staff-office"]:
        return {"status": 0, "msg": "Only Staff's can edit attendance data"}
    if field.user_type not in ["student","staff"]:
        return{"staus":0,'msg':"Invalid User type"}
    if field.user_type == "student":
        
        get_staff_cls = db.query(Classroom).filter(Classroom.class_advisor_id == get_user.id,Classroom.status == 1).first()
        if not get_staff_cls:
            return {"status": 0, "msg": "No class is associated with this staff"}
        get_cls_acad_id = db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.classroom_id == get_staff_cls.id,ClassAcademicAssociation.status == 1).first()
        if not get_cls_acad_id:
            return {"status": 0, "msg": "No academic association found for this class"}

        get_students = db.query(StudentClass).filter(StudentClass.class_academic_id == get_cls_acad_id.id,StudentClass.status == 1).all()
        valid_rolls = {s.roll_number: s.student_id for s in get_students}
        attendance_users = [
            (field.present_id, 1),
            (field.Absent_id, 0),
            (field.Half_morning, 2),
            (field.Half_afternoon, 3),
            (field.On_duty, 4)
        ]

        updated_rolls = []
        not_in_class = []

        for user_ids, status in attendance_users:
            if user_ids:
                for roll in user_ids:
                    if roll not in valid_rolls:
                        not_in_class.append(roll)
                        continue

                    student_id = valid_rolls[roll]
                    attendance_record = db.query(Attendance).filter(Attendance.user_id == student_id,Attendance.attendance_date == field.Attendance_date,Attendance.status == 1).first()
                    attendance_record.status = status
                    attendance_record.modified_by = get_user.id
                    updated_rolls.append(roll)

        db.commit()
        return {"status": 1,"msg": f"Updated Attendance for: {updated_rolls}","msg2": f"Not part of your class: {not_in_class}"}
    elif field.user_type == "staff":
        get_staff = db.query(User).filter(User.role == field.user_type, User.status == 1).all()
        valid_staff = [i.id for i in get_staff]

        existing_attendance = db.query(Attendance).filter(Attendance.attendance_date == field.Attendance_date).all()
        existing_map = {(i.user_id, i.attendance_date): i for i in existing_attendance}

        updated_staff = []
        not_found = []
        invalid_ids = []

        attendance_users = [
            (field.present_id, 1),
            (field.Absent_id, 0),
            (field.Half_morning, 2),
            (field.Half_afternoon, 3),
            (field.On_duty, 4)
        ]

        for user_ids, status in attendance_users:
            if user_ids:
                for staff_id in user_ids:
                    if staff_id not in valid_staff:
                        invalid_ids.append(staff_id)
                        continue

                    att_record = existing_map.get((staff_id, field.Attendance_date))
                    if not att_record:
                        not_found.append(staff_id)
                        continue

                    att_record.status = status
                    att_record.modified_by = get_user.id
                    updated_staff.append(staff_id)

        db.commit()
        return {"status": 1,"msg": f"Attendance Data Updated Successfully for the Staffs {updated_staff}","msg2": f"{not_found} These Staffs didn't have attendance previously","msg3": f"{invalid_ids} These Staff IDs are invalid"}

@router.post("/view_attendance_data", description="This Route is for View Attendance Data by their own Staff can view their Students Attendance while the Principal can view the staff's Attendance")
def view_attendance_data(field: attendance_schema.ViewAttendance, db: Session = Depends(get_db)):
    get_user = check_token_all(field.token, db)
    if isinstance(get_user, dict):
        return get_user
    def filter_by_date(query):
        if field.from_date:
            query = query.filter(Attendance.attendance_date >= field.from_date)
        if field.to_date:
            query = query.filter(Attendance.attendance_date <= field.to_date)
        return query
    if field.user_type == "student":
        if get_user.role in ["staff", "staff-office"]:
            classroom = db.query(Classroom).filter(Classroom.class_advisor_id == get_user.id, Classroom.status == 1).first()
            if not classroom:
                return {"status": 0, "msg": "No class associated with this staff"}
            assoc = db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.classroom_id == classroom.id,ClassAcademicAssociation.status == 1).first()
            students = db.query(StudentClass).filter(StudentClass.class_academic_id == assoc.id,StudentClass.status == 1).all()

            data = []
            for stu in students:
                att_q = db.query(Attendance, User).join(User, User.id == Attendance.user_id).filter(Attendance.user_id == stu.student_id)
                att_q = filter_by_date(att_q) 
                attendance_results = att_q.all()

                attendance_list = [row[0] for row in attendance_results]  
                user = db.query(User).filter(User.id == stu.student_id).first()

                counts = count_attendance(attendance_list)
                data.append({
                    "student_id": stu.student_id,
                    "student_name": f"{user.first_name} {user.last_name}",
                    "roll_number": stu.roll_number,
                    "attendance_summary": counts
                })
            return {"status": 1, "msg": "Student Attendance Fetched", "data": data}
        
        elif get_user.role == "student":
            att_q = db.query(Attendance).filter(Attendance.user_id == get_user.id)
            att_q = filter_by_date(att_q)
            attendance = att_q.all()
            counts = count_attendance(attendance)
            return {"status": 1, "msg": "Your Attendance Summary", "student_id": get_user.id,"student_name":get_user.first_name + " " + get_user.last_name, "data": counts}
        
    elif field.user_type in ["staff","staff-office"]:
        if get_user.role in ["staff", "staff-office"]:
            att_q = db.query(Attendance).filter(Attendance.user_id == get_user.id)
            att_q = filter_by_date(att_q)
            attendance = att_q.all()
            counts = count_attendance(attendance)
            return {"status": 1, "msg": "Your Attendance Summary", "staff_name": f"{get_user.first_name or ''} {get_user.last_name or ''}" if get_user else " ","data": counts}
        elif get_user.role == "principal":
            staffs = db.query(User).filter(User.role == "staff", User.status == 1).all()
            result = []
            for staff_id in staffs:
                att_q = db.query(Attendance).filter(Attendance.user_id == staff_id.id)
                att_q = filter_by_date(att_q)
                attendance = att_q.all()
                counts = count_attendance(attendance)
                result.append({
                    "staff_id": staff_id.id,
                    "name": staff_id.first_name + " " + staff_id.last_name,
                    "attendance_summary": counts
                })
            return {"status": 1, "msg": "All Staffs Attendance Fetched", "data": result}

    return {"status": 0, "msg": "Invalid user role or user_type"}



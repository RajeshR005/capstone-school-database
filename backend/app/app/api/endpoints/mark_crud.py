from fastapi import APIRouter,Depends,File,Form,UploadFile,requests
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

router=APIRouter(prefix="/marks")

@router.post("/add_mark",description="This Route is for the Class advisor who can add marks for students in their class")
def add_mark(token:str=Form(...),exam_allocation_id:int=Form(...),subject_allocation_id:int=Form(...),student_ids:str=Form(...),marks:str=Form(...),max_mark:int=Form(...),db:Session=Depends(get_db)):
    try:
        student_ids_list=[int(i.strip()) for i in student_ids.split(",") if i.strip()]
        marks_list=[int(i.strip()) for i in marks.split(",") if i.strip()]
    except ValueError:
        return {"status":0,"msg":"Invalid format in student_ids or marks. Must be comma-separated integers."}

    if len(student_ids_list) != len(marks_list):
        return {"status":0,"msg":"Mismatch in count of student_ids and marks"}

    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if get_user.role != "staff":
        return {"status":0,"msg":"Only staff members are allowed to add marks"}

    classroom=db.query(Classroom).filter(Classroom.class_advisor_id==get_user.id,Classroom.status==1).first()
    if not classroom:
        return {"status":0,"msg":"You are not assigned as class advisor for any class"}

    class_acad=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.classroom_id==classroom.id,ClassAcademicAssociation.status==1).first()
    if not class_acad:
        return {"status":0,"msg":"No academic association found for your class"}

    valid_students=db.query(StudentClass).filter(StudentClass.class_academic_id==class_acad.id,StudentClass.status==1).all()
    valid_ids=[s.student_id for s in valid_students]

    final_records=[]
    invalid_students=[]
    duplicate_entries=[]

    for i,student_id in enumerate(student_ids_list):
        if student_id not in valid_ids:
            invalid_students.append(student_id)
            continue
        exist_mark=db.query(Mark).filter(Mark.exam_allocation_id==exam_allocation_id,Mark.subject_allocation_id==subject_allocation_id,Mark.student_id==student_id).first()
        if exist_mark:
            duplicate_entries.append(student_id)
            continue

        record=Mark(
            exam_allocation_id=exam_allocation_id,
            subject_allocation_id=subject_allocation_id,
            student_id=student_id,
            mark_obtained=marks_list[i],
            max_mark=max_mark,
            created_by=get_user.id,
            modified_by=get_user.id
        )
        final_records.append(record)

    if final_records:
        db.add_all(final_records)
        db.commit()

    return {"status":1,"msg":"Marks Added Successfully","invalid_students":invalid_students,"duplicate_entries":duplicate_entries,"student_ids":[r.student_id for r in final_records]}

@router.post("/edit_mark",description="Edit marks for students by class advisor")
def edit_mark(token:str=Form(...),exam_allocation_id:int=Form(...),subject_allocation_id:int=Form(...),student_ids:str=Form(...),marks:str=Form(...),db:Session=Depends(get_db)):
    try:
        student_ids_list=[int(i.strip()) for i in student_ids.split(",") if i.strip()]
        marks_list=[int(i.strip()) for i in marks.split(",") if i.strip()]
    except ValueError:
        return {"status":0,"msg":"Invalid format. Use comma-separated integers for student_ids and marks."}

    if len(student_ids_list)!=len(marks_list):
        return {"status":0,"msg":"Mismatch in count of student_ids and marks"}

    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user

    if get_user.role!="staff":
        return {"status":0,"msg":"Only staff members are allowed to edit marks"}

    classroom=db.query(Classroom).filter(Classroom.class_advisor_id==get_user.id,Classroom.status==1).first()
    if not classroom:
        return {"status":0,"msg":"You are not assigned as class advisor for any class"}

    class_acad=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.classroom_id==classroom.id,ClassAcademicAssociation.status==1).first()
    if not class_acad:
        return {"status":0,"msg":"No academic association found for your class"}

    valid_students=db.query(StudentClass).filter(StudentClass.class_academic_id==class_acad.id,StudentClass.status==1).all()
    valid_ids=[s.student_id for s in valid_students]

    updated_students=[]
    invalid_students=[]
    not_found_entries=[]

    for i,student_id in enumerate(student_ids_list):
        if student_id not in valid_ids:
            invalid_students.append(student_id)
            continue

        existing_mark=db.query(Mark).filter(Mark.exam_allocation_id==exam_allocation_id,Mark.subject_allocation_id==subject_allocation_id,Mark.student_id==student_id).first()

        if not existing_mark:
            not_found_entries.append(student_id)
            continue

        existing_mark.mark_obtained=marks_list[i]
        existing_mark.modified_by=get_user.id
        updated_students.append(student_id)

    db.commit()

    return {"status":1,"msg":f"Marks updated for students: {updated_students}","invalid_students":invalid_students,"not_found_entries":not_found_entries}

@router.post('view_marks',description="This Route is for View the Marks of the students by themselves and by their class teachers")
def view_marks(token:str=Form(...),db:Session=Depends(get_db)):
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if get_user.role=="student":
        get_marks_data=db.query(Mark).filter(Mark.student_id==get_user.id,Mark.status==1).all()
        if not get_marks_data:
            return{"stauts":0,"msg":"No data available for the User"}
        get_cls_acad=db.query(StudentClass).filter(StudentClass.student_id==get_user.id).first()
        if not get_cls_acad:
            return{"status":0,"msg":"You are not associated with any class"}
        class_assoc=get_cls_acad.class_academic.classroom_id
        get_cls=db.query(ClassAcademicAssociation).filter(ClassAcademicAssociation.classroom_id==class_assoc).first()
        get_std=db.query(Standard).filter(Standard.id==get_cls.classroom.standard_id).first()
        get_sec=db.query(Section).filter(Section.id==get_cls.classroom.section_id).first()
        
        print(class_assoc)
        grouped_data=[]
        map_data={}
        for i in get_marks_data:
            
            exam_id=i.exam_allocation_id
            if exam_id not in map_data:
                exam_alloc_name=db.query(ExamAllocation).filter(ExamAllocation.id==i.exam_allocation_id).first()
                
                map_data[exam_id]={
                    "Exam Name":exam_alloc_name.exam.exam_name,
                    "subjects":[]
            }
            subj_alloc_name=db.query(SubjectAllocation).filter(SubjectAllocation.id==i.subject_allocation_id).first()
            
            map_data[exam_id]["subjects"].append(
                {
                "subject Name":subj_alloc_name.subject.subject_name,
                "mark_obtained":i.mark_obtained,
                "max_marks":i.max_mark
                }
            )
        grouped_data=list(map_data.values())
        return [
            {
                "student_id":get_user.id,
                "student Name":f"{get_user.first_name} {get_user.last_name}",
                "standard":get_std.std_name,
                "section":get_sec.section_name,
                "Mark_sheet":grouped_data
            }

        ]
    elif get_user.role=="staff":
        get_classroom=db.query(Classroom).join(Classroom.class_academics).filter(Classroom.class_advisor_id==get_user.id,Classroom.status==1).first()
        # return get_classroom.class_academics[0].id
        get_students=db.query(StudentClass).filter(StudentClass.class_academic_id==get_classroom.class_academics[0].id).all()

        final_list=[]
        for j in get_students:
            get_marks_data=db.query(Mark).filter(Mark.student_id==j.id,Mark.status==1).all()
            grouped_data=[]
            map_data={}
            for i in get_marks_data:
                
                exam_id=i.exam_allocation_id
                if exam_id not in map_data:
                    exam_alloc_name=db.query(ExamAllocation).filter(ExamAllocation.id==i.exam_allocation_id).first()
                    
                    map_data[exam_id]={
                        "Exam Name":exam_alloc_name.exam.exam_name,
                        "subjects":[]
                }
                subj_alloc_name=db.query(SubjectAllocation).filter(SubjectAllocation.id==i.subject_allocation_id).first()
                
                map_data[exam_id]["subjects"].append(
                    {
                    "subject Name":subj_alloc_name.subject.subject_name,
                    "mark_obtained":i.mark_obtained,
                    "max_marks":i.max_mark
                    }
                )
            grouped_data=list(map_data.values())
            final_list.append(
                {
                    "student_id":j.id,
                    "student Name":f"{j.student.first_name} {j.student.last_name}",
                    "Mark_sheet":grouped_data
                }

            )

        return final_list  
            

        

        
        
                        

                    
                        
                        
                    

                
                    
                




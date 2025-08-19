from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.api.deps import *
from sqlalchemy.orm import Session
from app.models import *
from app.utils import *

router=APIRouter(prefix="/project_submission")


@router.post("/add_project_report",description="This Route is used to Add the project Report or Record by the Students")
def add_project(token:str=Form(...),Subject_Name:str= Form(...),title:str=Form(...,description="Title of the Project"),file_description:str=Form(...,description="Add description of the Report"),upload_file:UploadFile=File(...,description="Upload your Project/Assessment File Here !"),db:Session=Depends(get_db)):
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if get_user.role!="student":
        return{"status":0,"msg":"Your are not Authorized to submit any Report"}
    get_subject_code=db.query(Subject).filter(Subject.subject_name==Subject_Name.capitalize(),Subject.status==1).first()
    save_full_path,file_exe=file_storage(upload_file,upload_file.filename,sub_folder="project_submissions")
    new_record=StudentSubmission(
        student_id=get_user.id,
        subject_code=get_subject_code.code,
        submission_type="project",
        title=title,
        description=file_description,
        file_path=save_full_path,
        created_by=get_user.id,
        modified_by=get_user.id
        )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return[{
        "status":1,
        "msg":"File Submitted Successfully",
        "subject_name":new_record.subject.subject_name,
        "subject_code":new_record.subject_code,
        "title":new_record.title,
        "file_description":new_record.description,
        "submitted_file":new_record.file_path,
        "Reference_id":new_record.id

    }]

@router.post("/edit_project_report",description="This Route is used to change the report details like file, title, description of the existing file")
def edit_project_report(token:str=Form(...),reference_id:str=Form(...,example="Enter the Reference ID"),title:Optional[str]=Form(None),description:Optional[str]=Form(None),new_file:Optional[UploadFile]=File(None),db:Session=Depends(get_db)):
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    get_exist_record=db.query(StudentSubmission).filter(StudentSubmission.id==reference_id,StudentSubmission.student_id==get_user.id,StudentSubmission.status==1).first()
    if not get_exist_record:
        return{"status":0,"msg":"No Project Record Found for this Reference ID"}
    if title:
        get_exist_record.title=title
    if description:
        get_exist_record.description=description
    if new_file:
        old_file_path = Path(get_exist_record.file_path)
        if old_file_path.exists():
            old_file_path.unlink()
        new_file_path, file_exe = file_storage(new_file, new_file.filename, sub_folder="project_submissions")
        get_exist_record.file_path=new_file_path

    db.commit()
    db.refresh(get_exist_record)
    return[
        {
            "status":0,
            "msg":"File Updated Sucessfully",
            "reference_id":get_exist_record.id,
            "title":get_exist_record.title,
            "description":get_exist_record.description,
            "uploaded_file":get_exist_record.file_path
        }
    ]

@router.post("view_project_report",description="This Route is used to view the project submission by students and staffs")
def view_project(token:str=Form(...),subject_name:Optional[str]=Form(None,description="Incase you want to view specific subject submission enter the subject name"),db:Session=Depends(get_db)):
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if get_user.role=="student":
        if subject_name:
            get_subject=db.query(Subject).filter(Subject.subject_name==subject_name.capitalize(),Subject.status==1).first()
            if not get_subject:
                return{"status":0,"msg":"The given subject file doesn't exist"}
            get_records=db.query(StudentSubmission).filter(StudentSubmission.student_id==get_user.id,StudentSubmission.subject_code==get_subject.code,StudentSubmission.status==1).first()
            return[
                {
                    "subject_name":get_subject.subject_name,
                    "subject_code":get_records.subject_code,
                    "title":get_records.title,
                    "description":get_records.description,
                    "file_path":get_records.file_path
                }
            ]
        
        else:
            get_records=db.query(StudentSubmission).filter(StudentSubmission.student_id==get_user.id,StudentSubmission.status==1).all()
            if not get_records:
                return{"status":0,"msg":"No Projects Submissions Found"}
            submission=[]
            for i in get_records:
                submission.append({
                        "title":i.title,
                        "subject_name":i.subject.subject_name,
                        "description":i.description,
                        "file":i.file_path
                }
                )
                
            return[
                {
                    "student_name":get_records[0].student.first_name,
                    "submissions":submission
                }
            ]
    


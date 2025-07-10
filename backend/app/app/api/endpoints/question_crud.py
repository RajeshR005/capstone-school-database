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

router=APIRouter(prefix="/Questions")

@router.post('/upload/questions')
def upload_questions(token:str=Form(...),exam_allocation_id:str=Form(...),subject_id:str=Form(...),questions:UploadFile=File(...),description:str=Form(...),db:Session=Depends(get_db)):
    save_full_path,file_exe=file_storage(questions,questions.filename,sub_folder="questions")
    get_user=check_token_all(token,db)
    if isinstance(get_user,dict):
        return get_user
    if get_user.role!="staff":
        return{"status":0,"msg":"You are not authorized to upload Questions Data"}
    record = db.query(QuestionPaper).filter(QuestionPaper.exam_allocation_id==exam_allocation_id,QuestionPaper.subject_id==subject_id, QuestionPaper.status == 1).first()
    if record:
        return {"status": 0, "msg": "question paper Already Exist in the DB you can use edit to change the file","exist_id":record.id}
    new_record = QuestionPaper(
        exam_allocation_id=exam_allocation_id,
        subject_id=subject_id,
        file_path=save_full_path,
        description=description,
        created_by=get_user.id,
        modified_by=get_user.id,
        
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    

    return {"message": "Question Paper uploaded and saved to database successfully","question_url": save_full_path,"question_id": new_record.id}

@router.post("/edit/questions", description="This Route is for Edit an already uploaded question file")
def edit_question_file(token: str = Form(...),question_id: int = Form(...),new_file: UploadFile = File(...),description: str = Form(...),db: Session = Depends(get_db)):
    get_user = check_token_all(token, db)
    if isinstance(get_user, dict):
        return get_user

    if get_user.role != "staff":
        return {"status": 0, "msg": "You are not authorized to edit Questions Data"}
    record = db.query(QuestionPaper).filter(QuestionPaper.id == question_id, QuestionPaper.status == 1).first()
    if not record:
        return {"status": 0, "msg": "No such question paper found in the DB"}

    old_file_path = Path(record.file_path)
    if old_file_path.exists():
        old_file_path.unlink()

    new_file_path, file_exe = file_storage(new_file, new_file.filename, sub_folder="questions")

    record.file_path = new_file_path
    record.description = description
    record.modified_by = get_user.id

    db.commit()
    db.refresh(record)

    return {"status": 1,"msg": "Question paper updated successfully","new_file_path": new_file_path,"record_id": record.id}

@router.post("/download/questions/", description="This Route is for Download question paper using question ID")
def download_question_file(token:str=Form(...),question_id:str=Form(...), db: Session = Depends(get_db)):
    get_user = check_token_all(token, db)
    if isinstance(get_user, dict):
        return get_user
    if get_user.role not in ["staff","student"]:
        return{"status":0,"msg":"You are not authorized to download file"}
    record = db.query(QuestionPaper).filter(QuestionPaper.id == question_id, QuestionPaper.status == -1).first()
    if not record:
        return {"status": 0, "msg": "No Question paper found in the Database"}

    file_path = Path(record.file_path)
    if not file_path.exists():
        return {"status": 0, "msg": "File does not exist on server"}

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=file_path.name
    )

@router.post('/view_all_questions_active',description="This Route is used for View Active Question Papers")
def view_all_questions_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_user = check_token_all(token, db)
    if isinstance(get_user, dict):
        return get_user
    if get_user.role not in ["staff"]:
        return{"status":0,"msg":"You are not authorized to View Current Question Papers"}
    get_data=db.query(QuestionPaper,Subject).join(QuestionPaper.subject).filter(QuestionPaper.status==1).all()
    if not get_data:
        return{"status":0,"msg":"No Active Questions papers Allocated for any Exams"}
    return[{
        "Question_id":i[0].id,
        "Exam_allocated_id":i[0].exam_allocation_id,
        "Subject Name":i[1].subject_name,
        "question url":i[0].file_path,
        "Description":i[0].description
    }
    for i in get_data
    ]

@router.post('/view_all_questions_in_active',description="This Route is used for View Active Question Papers")
def view_all_questions_in_active(token:str=Form(...),db:Session=Depends(get_db)):
    get_user = check_token_all(token, db)
    if isinstance(get_user, dict):
        return get_user
    if get_user.role not in ["staff"]:
        return{"status":0,"msg":"You are not authorized view all inactive question papers"}
    get_data=db.query(QuestionPaper,Subject).join(QuestionPaper.subject).filter(QuestionPaper.status==-1).all()
    if not get_data:
        return{"status":0,"msg":"No In-Active Questions papers Allocated for any Exams"}
    return[{
        "Question_id":i[0].id,
        "Exam_allocated_id":i[0].exam_allocation_id,
        "Subject Name":i[1].subject_name,
        "question url":i[0].file_path,
        "Description":i[0].description
    }
    for i in get_data
    ]

@router.post('/Change_status_question_paper',description="This Route is for Change the status of question paper After the Exam so the Students can download the file for reference ")
def change_status_question_paper(token:str=Form(...),Question_id:int=Form(...),change_status:int=Form(...,description="The Status code are 1 = Activate , -1 = Inactive, 2 = delete"),db:Session=Depends(get_db)):
    get_user = check_token_all(token, db)
    if isinstance(get_user, dict):
        return get_user
    if get_user.role not in ["staff"]:
        return{"status":0,"msg":"You are not authorized In-Active question papers"}
    get_data=db.query(QuestionPaper).filter(QuestionPaper.id==Question_id).first()
    if not get_data:
        return{"status":0,"msg":"No Question paper Data is found in the DB"}
    if change_status not in [1,2,-1]:
        return{"status":0,"msg":"Invalid Status code"}
    get_data.status=change_status
    db.commit()
    
    if change_status==1:
        return{"status":1,"msg":f"{get_data.id} Activated Sucessful"}
    elif change_status==0:
        return{"status":1,"msg":f"{get_data.id} Deleted Sucessful"}
    elif change_status==-1:
        return{'status':1,"msg":f"{get_data.id} In-Activated Sucessful"}
    

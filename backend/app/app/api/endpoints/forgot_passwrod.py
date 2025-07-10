from pydantic import EmailStr
from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import get_db,check_token_all,count_attendance
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime, timezone
from app.utils import *
from sqlalchemy import or_
from app.schemas import user_schema,login_schema,attendance_schema
from typing import Optional
from app.utils import send_email_otp
from datetime import timedelta
router = APIRouter(prefix="/Authentication")

@router.post("/forgot_password",description="This Route is for Forgot password they can get the otp to reset their password")
def forgot_password(email: EmailStr = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"status":0,"msg":"Email not found in the DB"}
    otp = str(random.randint(100000, 999999))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    otp_entry = ForgotPasswordOTP(user_id=user.id,otp=otp,expires_at=expires_at)

    db.add(otp_entry)
    db.commit()

    send_email_otp(to=email, otp=otp)
    return {"status":1,"msg":"OTP sent to your email"}

@router.post('/verify_otp',description="This Route is used to validate your otp")
def verify_otp(otp:str=Form(...),db:Session=Depends(get_db)):
    
    otp_entry = db.query(ForgotPasswordOTP).filter(ForgotPasswordOTP.otp == otp).order_by(ForgotPasswordOTP.created_at.desc()).first()
    if not otp_entry:
        return {"status": 0, "msg": "Invalid OTP or Expired OTP"}
    return{"status":1,"msg":"This is Valid OTP"}

@router.post("/reset-password",description="This Route is for Reset their password after they get the otp they enter if it is valid they can reset the password")
def reset_password(Email: EmailStr = Form(...),otp: str = Form(...),new_password: str = Form(...),confirm_password:str=Form(...),db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == Email).first()
    if not user:
        return {"status": 0, "msg": "User not found"}

    otp_entry = db.query(ForgotPasswordOTP).filter(ForgotPasswordOTP.user_id == user.id).order_by(ForgotPasswordOTP.created_at.desc()).first()

    if not otp_entry:
        return {"status": 0, "msg": "No OTP found for this user"}
    if otp_entry.otp != otp:
        return {"status": 0, "msg": "Invalid OTP"}
    if otp_entry.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return {"status": 0,"msg":"OTP has expired"}

    if not new_password==confirm_password:
        return{"status":0,"msg":" new_password and confirm Password doesn't match"}
    user.password = get_password_hash(new_password)

    db.delete(otp_entry)

    db.commit()
    return {"status": 1, "msg": "Password reset successful"}

@router.post("/resend-otp")
def resend_otp(email: EmailStr = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"status": 0, "msg": "User not found"}
    otp = str(random.randint(100000, 999999))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    otp_entry = ForgotPasswordOTP(user_id=user.id, otp=otp, expires_at=expires_at)
    db.add(otp_entry)
    db.commit()
    send_email_otp(to=email, otp=otp)
    return {"status": 1, "msg": "OTP resent successfully"}

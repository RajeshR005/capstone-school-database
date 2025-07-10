from typing import Optional,List
from pydantic import BaseModel
# from sqlalchemy.orm import 
from datetime import date,time,timedelta,datetime



class AttendanceData(BaseModel):
    token: str
    user_type:str
    present_id: Optional[List[int]] = []
    Absent_id: Optional[List[int]] = []
    Half_morning: Optional[List[int]] = []
    Half_afternoon: Optional[List[int]] = []
    On_duty: Optional[List[int]] = []
    Attendance_date: date

class ViewAttendance(BaseModel):
    token: str
    user_type: str  # "student" or "staff"
    from_date: Optional[date] = None
    to_date: Optional[date] = None
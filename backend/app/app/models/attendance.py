from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    attendance_date = Column(Date)
    # class_academic_id = Column(Integer, ForeignKey("class_academic_associations.id"))

    # 0 - Absent, 1 - Present, 2 - Half Morning, 3 - Half Afternoon, 4 - On Duty (OD)
    status = Column(Integer)
    check_in = Column(Time)  
    check_out = Column(Time)  
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))
    # class_academic = relationship("ClassAcademicAssociation", back_populates="attendance_records")

    user = relationship("User", foreign_keys=[user_id], back_populates="attendance_records")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_attendance_records")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_attendance_records")

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class StudentSubmission(Base):
    __tablename__ = 'student_submissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('users.id'))
    subject_code = Column(String(20), ForeignKey('subjects.code'))  #
    submission_type = Column(String(50))  
    title = Column(String(255))
    
    description = Column(String(255))
    file_path = Column(String(500))  
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    student = relationship("User", foreign_keys=[student_id])
    creator = relationship("User", foreign_keys=[created_by])
    modifier = relationship("User", foreign_keys=[modified_by])
    subject = relationship("Subject", back_populates="student_submissions")

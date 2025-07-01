from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Exam(Base):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_name = Column(String(100)) 
    status = Column(Integer, default=1) 
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))


    exam_allocations = relationship("ExamAllocation", back_populates="exam")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_exams")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_exams")

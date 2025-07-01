from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class QuestionPaper(Base):
    __tablename__ = 'question_papers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    exam_allocation_id = Column(Integer, ForeignKey('exam_allocations.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    file_path = Column(String(500)) 
    description = Column(String(255))
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    exam_allocation = relationship("ExamAllocation", back_populates="question_papers")
    subject = relationship("Subject", back_populates="question_papers")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_question_papers")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_question_papers")

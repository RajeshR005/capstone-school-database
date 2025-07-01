from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Mark(Base):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    exam_allocation_id = Column(Integer, ForeignKey('exam_allocations.id'))
    subject_allocation_id = Column(Integer, ForeignKey('subject_allocations.id'))
    student_id = Column(Integer, ForeignKey('users.id'))
    mark_obtained = Column(Integer)
    max_mark = Column(Integer)
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    exam_allocation = relationship("ExamAllocation", back_populates="marks")
    subject_allocation = relationship("SubjectAllocation", back_populates="marks")
    student = relationship("User", back_populates="marks", foreign_keys=[student_id])
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_marks")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_marks")

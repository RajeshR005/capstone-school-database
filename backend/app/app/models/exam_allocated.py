from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class ExamAllocation(Base):
    __tablename__ = 'exam_allocations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    class_academic_id = Column(Integer, ForeignKey('class_academic_associations.id'))
    exam_id = Column(Integer, ForeignKey('exams.id'))
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    class_academic = relationship("ClassAcademicAssociation", back_populates="exam_allocations")
    exam = relationship("Exam", back_populates="exam_allocations")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_exam_allocations")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_exam_allocations")
    marks = relationship("Mark", back_populates="exam_allocation")
    question_papers = relationship("QuestionPaper", back_populates="exam_allocation")



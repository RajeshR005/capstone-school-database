from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(100))
    code = Column(String(20),unique=True)
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_subjects")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_subjects")
    allocations = relationship("SubjectAllocation", back_populates="subject")
    standard_term_resources = relationship("SubjectStandardTermResource", back_populates="subject")
    allocations = relationship("SubjectAllocation", back_populates="subject")
    time_table_entries = relationship("TimeTable", back_populates="subject")
    question_papers = relationship("QuestionPaper", back_populates="subject")
    student_submissions = relationship("StudentSubmission", back_populates="subject")





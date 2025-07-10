from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class Standard(Base):
    __tablename__ = 'standards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    std_name = Column(String(20))
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    classrooms = relationship("Classroom", back_populates="standard")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_standards")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_standards")
    term_subject_resources = relationship("SubjectStandardTermResource", back_populates="standard")
    fee_structures = relationship("FeeStructure", back_populates="standard")
    exam_allocations=relationship("ExamAllocation",back_populates="standard")


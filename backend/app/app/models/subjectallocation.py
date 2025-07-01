from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class SubjectAllocation(Base):
    __tablename__ = 'subject_allocations'

    id = Column(Integer, primary_key=True, autoincrement=True)

    class_academic_id = Column(Integer, ForeignKey('class_academic_associations.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    staff_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    class_academic = relationship("ClassAcademicAssociation", back_populates="subject_allocations")
    subject = relationship("Subject", back_populates="allocations")
    staff = relationship("User", foreign_keys=[staff_id],back_populates="subject_allocations")
    
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_subject_allocations")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_subject_allocations")
    marks = relationship("Mark", back_populates="subject_allocation")
    # attendance_records = relationship("Attendance", back_populates="subject_allocation")



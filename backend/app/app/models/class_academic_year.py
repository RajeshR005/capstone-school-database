from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime



class ClassAcademicAssociation(Base):
    __tablename__ = 'class_academic_associations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    classroom_id = Column(Integer, ForeignKey('classrooms.id'))
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))



    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_class_academics")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_class_academics")
    subject_allocations = relationship("SubjectAllocation", back_populates="class_academic")
    group = relationship("Group", back_populates="class_academics")
    students = relationship("StudentClass", back_populates="class_academic")
    # exam_allocations = relationship("ExamAllocation", back_populates="class_academic")
    # attendance_records = relationship("Attendance", back_populates="class_academic")
    time_table_entries = relationship("TimeTable", back_populates="class_academic")
    # fee_structures = relationship("FeeStructure", back_populates="class_academic")
    academic_year = relationship("AcademicYear", back_populates="class_academic")

    classroom = relationship("Classroom", back_populates="class_academics")



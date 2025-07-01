from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base


class FeeStructure(Base):
    __tablename__ = 'fee_structures'

    id = Column(Integer, primary_key=True, autoincrement=True)

    academic_year_id = Column(Integer, ForeignKey('academic_years.id'))
    standard_id = Column(Integer, ForeignKey('standards.id'))  
    group_id = Column(Integer, ForeignKey('groups.id'))
    term_id = Column(Integer, ForeignKey('terms.id'))
    

    fee_type = Column(String(100))  
    amount = Column(Float)

    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    academic_year = relationship("AcademicYear", back_populates="fee_structures")
    standard = relationship("Standard", back_populates="fee_structures")
    group = relationship("Group", back_populates="fee_structures")
    term = relationship("Term", back_populates="fee_structures")

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_fee_structures")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_fee_structures")

    student_fees = relationship("StudentFee", back_populates="fee_structure")
    student_scholarships = relationship("StudentScholarship", back_populates="fee_structure")


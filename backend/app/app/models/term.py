from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Term(Base):
    __tablename__ = 'terms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    term_name = Column(String(100))
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'))
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    academic_year = relationship("AcademicYear", back_populates="terms")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_terms")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_terms")
    standard_subject_resources = relationship("SubjectStandardTermResource", back_populates="term")

    fee_structures = relationship("FeeStructure", back_populates="term")





from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class AcademicYear(Base):
    __tablename__ = 'academic_years'

    id = Column(Integer, primary_key=True, autoincrement=True)
    academic_year = Column(String(20))
    is_current = Column(Integer,default=1)
    status = Column(Integer, default=1)
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    class_academic = relationship("ClassAcademicAssociation", back_populates="academic_year")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_academic_years")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_academic_years")
    terms = relationship("Term", back_populates="academic_year")
    fee_structures = relationship("FeeStructure", back_populates="academic_year")
    




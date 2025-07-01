from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base




class StudentScholarship(Base):
    __tablename__ = 'student_scholarships'

    id = Column(Integer, primary_key=True, autoincrement=True)

    student_id = Column(Integer, ForeignKey('users.id'))
    scholarship_id = Column(Integer, ForeignKey('scholarships.id'))
    fee_structure_id = Column(Integer, ForeignKey('fee_structures.id'))  

    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    student = relationship("User", foreign_keys=[student_id], back_populates="student_scholarships")
    scholarship = relationship("Scholarship", back_populates="student_scholarships")
    fee_structure = relationship("FeeStructure", back_populates="student_scholarships")

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_student_scholarships")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_student_scholarships")

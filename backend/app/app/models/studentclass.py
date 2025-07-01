from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class StudentClass(Base):
    __tablename__ = 'student_classes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    student_id = Column(Integer, ForeignKey('users.id'))
    class_academic_id = Column(Integer, ForeignKey('class_academic_associations.id'))
    roll_number = Column(Integer)
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    student = relationship("User", back_populates="student_class", foreign_keys=[student_id])
    class_academic = relationship("ClassAcademicAssociation", back_populates="students")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_student_classes")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_student_classes")

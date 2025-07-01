from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Classroom(Base):
    __tablename__ = 'classrooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    standard_id = Column(Integer, ForeignKey('standards.id'))
    section_id = Column(Integer, ForeignKey('sections.id'))
    class_advisor_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    standard = relationship("Standard", back_populates="classrooms")
    section = relationship("Section", back_populates="classrooms")
    class_advisor = relationship("User", foreign_keys=[class_advisor_id], back_populates="advised_classes")
    class_academics = relationship("ClassAcademicAssociation", back_populates="classroom")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_classrooms")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_classrooms")

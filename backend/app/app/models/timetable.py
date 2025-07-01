from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class TimeTable(Base):
    __tablename__ = 'time_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    class_academic_id = Column(Integer, ForeignKey('class_academic_associations.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    staff_id = Column(Integer, ForeignKey('users.id'))
    day_of_week = Column(String(20))  
    period_number = Column(Integer)   
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    class_academic = relationship("ClassAcademicAssociation", back_populates="time_table_entries")
    subject = relationship("Subject", back_populates="time_table_entries")
    staff = relationship("User", back_populates="time_table_entries", foreign_keys=[staff_id])
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_time_table_entries")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_time_table_entries")

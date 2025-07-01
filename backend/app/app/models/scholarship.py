from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Scholarship(Base):
    __tablename__ = 'scholarships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))  
    description = Column(String(255))
    amount = Column(Float)  
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_scholarships")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_scholarships")
    student_scholarships = relationship("StudentScholarship", back_populates="scholarship")

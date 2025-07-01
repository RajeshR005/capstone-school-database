from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime
 

class SubjectStandardTermResource(Base):
    __tablename__ = 'subject_standard_term_resources'

    id = Column(Integer, primary_key=True, autoincrement=True)

    standard_id = Column(Integer, ForeignKey('standards.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    term_id = Column(Integer, ForeignKey('terms.id'))
    ebook_url = Column(String(255))  
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    standard = relationship("Standard", back_populates="term_subject_resources")
    subject = relationship("Subject", back_populates="standard_term_resources")
    term = relationship("Term", back_populates="standard_subject_resources")

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_standard_subject_resources")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_standard_subject_resources")

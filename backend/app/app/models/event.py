from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(255))
    description = Column(String(500))
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String(255))
    organized_by = Column(Integer, ForeignKey('users.id'))

    status = Column(Integer, default=1)  
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    organizer = relationship("User", foreign_keys=[organized_by], back_populates="organized_events")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_events")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_events")

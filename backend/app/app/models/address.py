from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    current_address = Column(String(255))
    current_city = Column(String(100))
    current_pincode = Column(String(20))
    permanent_address = Column(String(255))
    permanent_city = Column(String(100))
    permanent_pincode = Column(String(20))
    state = Column(String(100))
    country = Column(String(100))
    status = Column(Integer, default=1) 
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer,ForeignKey('users.id'))  
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer,ForeignKey('users.id'))

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_addresses")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_addresses")


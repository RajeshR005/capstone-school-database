from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base
from datetime import datetime, timezone

class Leave(Base):
    __tablename__ = 'leave_requests'

    leave_id = Column(Integer, primary_key=True, autoincrement=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    from_date = Column(Date)
    to_date = Column(Date)
    reason = Column(String(255))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    modified_by = Column(Integer, ForeignKey("users.id"))
    modified_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="leave_requests", foreign_keys=[user_id])
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_leave_requests")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_leave_requests")

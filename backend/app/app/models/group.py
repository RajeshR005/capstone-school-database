from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(100), nullable=False)  # e.g., Biology, Computer Science, Commerce
    description = Column(String(255), nullable=True)

    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", foreign_keys=[created_by], back_populates="created_groups")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_groups")
    class_academics = relationship("ClassAcademicAssociation", back_populates="group")
    fee_structures = relationship("FeeStructure", back_populates="group")
    



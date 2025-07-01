from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class StudentFee(Base):
    __tablename__ = 'student_fees'

    id = Column(Integer, primary_key=True, autoincrement=True)

    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey('fee_structures.id'), nullable=False)

    total_amount = Column(Float, nullable=False)          
    scholarship_amount = Column(Float, default=0.0)    
    paid_amount = Column(Float, default=0.0)              
    balance_amount = Column(Float, default=0.0)           

    status = Column(Integer, default=1)  
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    student = relationship("User", foreign_keys=[student_id], back_populates="student_fees")
    fee_structure = relationship("FeeStructure", back_populates="student_fees")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_student_fees")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_student_fees")
    fee_payments = relationship("FeePayment", back_populates="student_fee")

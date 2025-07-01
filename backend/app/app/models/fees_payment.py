from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class FeePayment(Base):
    __tablename__ = 'fee_payments'

    id = Column(Integer, primary_key=True, autoincrement=True)

    student_fee_id = Column(Integer, ForeignKey('student_fees.id'))
    amount_paid = Column(Float)
    payment_mode = Column(String(50))  
    payment_date = Column(DateTime, default=datetime.now)

    status = Column(Integer, default=1)  
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(Integer, ForeignKey('users.id'))

    student_fee = relationship("StudentFee", back_populates="fee_payments")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_fee_payments")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_fee_payments")

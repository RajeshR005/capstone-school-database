
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.db.base_class import Base

class ForgotPasswordOTP(Base):
    __tablename__ = "forgot_password_otp"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    otp = Column(String(6), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)



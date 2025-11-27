
from sqlalchemy import Column, Integer, String, Boolean

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    otp_secret = Column(String, nullable=True)
    otp_enabled = Column(Boolean, default=False)
    otp_auth_url = Column(String, nullable=True)

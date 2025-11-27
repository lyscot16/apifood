
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    products = relationship("Product", back_populates="company")

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    risk_score = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="cases")

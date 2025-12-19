from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class CaseWallet(Base):
    __tablename__ = "case_wallets"

    case_id = Column(Integer, ForeignKey("cases.id"), primary_key=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), primary_key=True)

    confidence = Column(Integer)
    note = Column(String)
    source = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    case = relationship("Case", back_populates="wallet_links")
    wallet = relationship("Wallet", back_populates="case_links")

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.case_wallet import CaseWallet

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True, nullable=False)
    label = Column(String, nullable=True)
    is_flagged = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship(
        "User",
        back_populates="wallets"
    )

    case_links = relationship(
        "CaseWallet",
        back_populates="wallet",
        cascade="all, delete-orphan"
    )

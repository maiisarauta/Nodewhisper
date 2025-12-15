from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

case_wallets = Table(
    "case_wallets",
    Base.metadata,
    Column("case_id", ForeignKey("cases.id"), primary_key=True),
    Column("wallet_id", ForeignKey("wallets.id"), primary_key=True),
)

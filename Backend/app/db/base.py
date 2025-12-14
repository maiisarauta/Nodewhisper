from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User
from app.models.wallet import Wallet
from app.models.case import Case

__all__ = ["Base", "User", "Wallet", "Case"]

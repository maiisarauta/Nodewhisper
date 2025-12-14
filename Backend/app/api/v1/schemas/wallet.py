from pydantic import BaseModel
from typing import Optional

class WalletCreate(BaseModel):
    address: str
    label: Optional[str] = None

class WalletUpdate(BaseModel):
    label: Optional[str] = None
    is_flagged: Optional[bool] = None

class WalletOut(BaseModel):
    id: int
    address: str
    label: Optional[str]
    is_flagged: bool

    class Config:
        from_attributes = True

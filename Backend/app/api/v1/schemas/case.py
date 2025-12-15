from pydantic import BaseModel
from typing import List, Optional

class CaseCreate(BaseModel):
    title: str
    description: Optional[str] = None

class CaseOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    risk_score: int

    class Config:
        from_attributes = True

class AttachWallets(BaseModel):
    wallet_ids: List[int]

class AttachWalletsSchema(BaseModel):
    wallet_ids: List[int]

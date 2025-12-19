from pydantic import BaseModel
from typing import Optional

class AttachWalletEvidenceSchema(BaseModel):
    wallet_id: int
    confidence: int = 50
    note: Optional[str] = None
    source: Optional[str] = None

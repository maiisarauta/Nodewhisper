from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class CaseCreate(BaseModel):
    title: str
    description: Optional[str] = None

class CaseOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    risk_score: int

    model_config = ConfigDict(from_attributes=True)

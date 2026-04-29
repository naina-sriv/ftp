from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class VoteBase(BaseModel):
    issue_id: int
    value: Literal[1, -1]

class VoteCreate(VoteBase):
    pass
    
class VoteResponse(VoteBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
    
    

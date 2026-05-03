from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CommentBase(BaseModel):
    content:str = Field(..., min_length=1, max_length=500)
    issue_id:int

class CommentCreate(CommentBase):
    pass
    
class CommentResponse(CommentBase):
    created_at:datetime
    user_id: int
    id:int
    
    class Config:
        from_attributes = True

    
    

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class IssueBase(BaseModel):
    title: str
    content: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address_text: Optional[str] = None


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    address_text: Optional[str] = None


class IssueResponse(IssueBase):
    id: int
    status: str
    user_id: int
    created_at: datetime
    threshold_reached: bool
    vote_count: int

    class Config:
        from_attributes = True
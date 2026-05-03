from pydantic import BaseModel

class ConstituencyBase(BaseModel):
    name: str
    state: str
    pincode: str
    
class ConstituencyResponse(ConstituencyBase):
    id: int
    class Config:
        from_attributes = True
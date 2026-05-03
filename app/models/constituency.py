from sqlalchemy import Column, Integer, String
from app.db import Base

class Constituency(Base):
    __tablename__ = "constituencies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    state = Column(String, nullable=False)
    pincode = Column(String, nullable=False)
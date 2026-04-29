from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True, index=True)
    
    first_name=Column(String, nullable=False)
    last_name=Column(String, nullable=True)
    email=Column(String,nullable=False, unique=True)
    password=Column(String, nullable=False)
    
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    
    
    
    
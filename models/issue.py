from .db import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Issue(Base):
    __tablename__="issues"
    
    id=Column(Interger, primary_key=True,nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address_text = Column(String, nullable=True)
    
    status = Column(String, default="open")
    created_at=Column(DateTime(timezone=True),nullable=False,server_default='now()')
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
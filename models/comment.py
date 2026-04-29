from .db import Base
from sqlalchemy import Column, Integer, String,ForeignKey

class Comment(Base):
    __tablename__="comments"
    id=Column(Integer, primary_key=True, index=True)
    content=Column(String,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    issue_id=Column(Integer,ForeignKey("issues.id"),nullable=False)

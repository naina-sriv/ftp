from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.db import Base

class Vote(Base):
    __tablename__="votes"
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    issue_id=Column(Integer,ForeignKey("issues.id"),nullable=False)
    __table_args__ = (UniqueConstraint('user_id', 'issue_id', name='unique_user_issue_vote'),)
    
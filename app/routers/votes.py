from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.vote import Vote
from app.core.dependencies import get_current_user
from app.db import get_db
from app.schema.vote import VoteCreate

router=APIRouter(prefix="/votes",tags=["Votes"])

@router.post("/")
def create_vote(vote: VoteCreate, db: Session= Depends(get_db), current_user= Depends(get_current_user)):
    new_vote=Vote(**vote.dict())
    db.add(new_vote)
    

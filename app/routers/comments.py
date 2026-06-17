from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.comment import Comment
from app.models.issue import Issue
from app.schema.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/issues/{issue_id}/comments", tags=["Comments"])

@router.get("/", response_model=List[CommentResponse])
def get_comments(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(
        Issue.id == issue_id,
        Issue.constituency_id == current_user.constituency_id
    ).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    comments = (
        db.query(Comment)
        .filter(Comment.issue_id == issue_id)
        .order_by(Comment.created_at.desc())
        .all()
    )
    return comments

@router.post("/", response_model=CommentResponse, status_code=201)
def create_comment(
    issue_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(
        Issue.id == issue_id,
        Issue.constituency_id == current_user.constituency_id
    ).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    comment = Comment(
        content=payload.content,
        user_id=current_user.id,
        issue_id=issue_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
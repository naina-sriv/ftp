from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db import get_db, SessionLocal
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.issue import Issue
from app.models.vote import Vote
from app.schema.vote import VoteResponse

router = APIRouter(prefix="/issues/{issue_id}", tags=["Votes"])

def escalate_if_threshold_met(issue_id: int):
    """Check vote count and escalate if threshold crossed. Runs in background."""
    db = SessionLocal()
    try:
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue or issue.threshold_reached:
            return

        vote_count = db.query(Vote).filter(Vote.issue_id == issue_id).count()
        THRESHOLD = 5  # you can move this to config.py later

        if vote_count >= THRESHOLD and not issue.threshold_reached:
            issue.threshold_reached = True
            if issue.status == "open":
                issue.status = "escalated"
            db.commit()
    finally:
        db.close()


@router.post("/vote", response_model=VoteResponse, status_code=201)
def vote_on_issue(
    issue_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(
        Issue.id == issue_id,
        Issue.constituency_id == current_user.constituency_id
    ).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")


    existing = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.issue_id == issue_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="You have already voted on this issue")

    # Create vote
    vote = Vote(user_id=current_user.id, issue_id=issue_id)
    db.add(vote)

    issue.vote_count += 1
    db.commit()
    db.refresh(vote)

    background_tasks.add_task(escalate_if_threshold_met, issue_id)

    return vote
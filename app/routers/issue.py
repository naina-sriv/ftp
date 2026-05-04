from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.issue import Issue
from app.core.dependencies import get_current_user
from app.db import get_db
from app.schema.issue import IssueResponse, IssueCreate, IssueUpdate

router=APIRouter(prefix="/issues",tags=["Issues"])

@router.get("/", response_model=list[IssueResponse])
def get_issues(db: Session= Depends(get_db),current_user = Depends(get_current_user)):
    issues=db.query(Issue).filter(Issue.constituency_id==current_user.constituency_id).all()
    return issues

@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue_by_id(issue_id:int, db: Session= Depends(get_db),current_user = Depends(get_current_user)):
    issue=db.query(Issue).filter(
        current_user.constituency_id==Issue.constituency_id,
        Issue.id==issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="No such issue found.")
    return issue

@router.post("/", response_model=IssueResponse)
def create_issue(issue: IssueCreate, db: Session=Depends(get_db), current_user= Depends(get_current_user)):
    new_issue=Issue(**issue.dict(),
                    constituency_id=current_user.constituency_id,
                    user_id=current_user.id)
    db.add(new_issue)
    db.commit() 
    db.refresh(new_issue)
    return new_issue

@router.delete("/{issue_id}", status_code=204)
def delete_issue(issue_id:int, db: Session= Depends(get_db), current_user= Depends(get_current_user)):
    issue=db.query(Issue).filter(
        Issue.id==issue_id,
        Issue.user_id==current_user.id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="No such issue found or you don't have permission to delete it.")
    db.delete(issue)
    db.commit()
    return None

@router.put("/{issue_id}", response_model=IssueResponse)
def update(issue_id:int, updated_issue:IssueUpdate, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    if issue.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorised")
    for key, value in updated_issue.dict(exclude_unset=True).items():
        setattr(issue, key, value)
    db.commit()
    db.refresh(issue)
    return issue
    
    
              
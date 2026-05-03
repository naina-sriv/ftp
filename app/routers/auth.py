from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schema.user import UserCreate, UserResponse, UserLogin
from app.schema.token import Token
from app.core.security import hash
from app.models.user import User
from app.core.security import create_token, verify

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register",response_model=UserResponse, status_code=201)
def user_register(user: UserCreate, db:Session=Depends(get_db)):
    email_check=db.query(User).filter(User.email==user.email).first()
    if email_check is not None:
        raise HTTPException(status_code=409)
    new_user=User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hash(user.password),
        constituency_id=user.constituency_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@router.post("/login", response_model=Token)
def user_login(user: UserLogin, db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if verify(user.password,db_user.hashed_password):
        token=create_token(
            {   "user_id": db_user.id,
                "constituency_id": db_user.constituency_id
            }
        )
    else:
        raise HTTPException(status_code=401, detail="Invalid Credntials")
    
    return {"access_token":token, "token_type":"bearer"}      
    
    
    
    
    
    
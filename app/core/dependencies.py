import app.core.security as security
import app.models.user as user_model
from app.db import get_db
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    payload=security.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401)
    user_id=payload["user_id"]
    if user_id is None:
        raise HTTPException(status_code=401)
    user=db.query(user_model.User).filter(user_model.User.id==int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401)
    return user
    
    
    
    
    
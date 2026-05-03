from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import UTC, datetime, timedelta
from app.core.config import settings



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash(pwd:str)->str:
    return pwd_context.hash(pwd)

def verify(pwd:str, hashed:str)->bool:
    return pwd_context.verify(pwd,hashed)

def create_token(data: dict)->str:
    token=data.copy()
    token["exp"]=datetime.now(UTC)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token["iat"]=datetime.now(UTC)
    return jwt.encode(token,settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token:str):
    try:
        return jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    except InvalidTokenError:
        return None


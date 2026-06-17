from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.issue import router as issue_router
from app.db import engine, Base
from app.models import user, issue, vote, comment, constituency

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(issue_router)

@app.get("/")
def root():
    return {"message": "Hello World"}
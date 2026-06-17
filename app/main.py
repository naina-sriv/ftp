from fastapi import FastAPI
from app.routers import auth, issue, comments, votes
from app.db import engine, Base
from app.models import user, issue, vote, comment, constituency

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(issue.router)
app.include_router(comments.router)   
app.include_router(votes.router)      

@app.get("/")
def root():
    return {"message": "Hello World"}
from fastapi import FastAPI
from app.routers import auth
from app.db import engine, Base
from app.models import user, issue, vote, comment, constituency

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
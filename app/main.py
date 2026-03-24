from fastapi import FastAPI
from app.routes import upload, search

app = FastAPI()

app.include_router(upload.router)
app.include_router(search.router)
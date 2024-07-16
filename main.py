from fastapi import FastAPI,APIRouter

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api import upload
from config import get_config
from db import db
app = FastAPI()

app.include_router(upload.router)


@app.on_event("startup")
async def startup():
    config = get_config()
    await db.connect_to_database(path=config.db_path)

@app.get("/")
async def home():
    return {"HELLO" : "GET"}
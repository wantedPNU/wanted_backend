from fastapi import FastAPI,APIRouter

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api import upload

app = FastAPI()

app.include_router(upload.router)



@app.get("/")
async def home():
    return {"HELLO" : "GET"}
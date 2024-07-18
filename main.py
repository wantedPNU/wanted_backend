from fastapi import FastAPI,APIRouter,Form

# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
from api import upload
from config.config import initiate_database
# from controller.user_controller import UserController

from urllib.parse import quote

app = FastAPI()

app.include_router(upload.router)


## 전체적인 구조 mvc 패턴으로 변경해야함

@app.get("/")
async def home():
    return {"message" : "welcome to wanted_backend"}



@app.on_event("startup")
async def on_app_start():
	await initiate_database()

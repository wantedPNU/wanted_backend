from fastapi import FastAPI
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
from api import setting,query, video,inference
# from config.config import initiate_database
from database import db_manager
# from controller.user_controller import UserController

from urllib.parse import quote

app = FastAPI()

app.include_router(video.router)
app.include_router(setting.router)
app.include_router(query.router)
app.include_router(inference.router)

## 전체적인 구조 mvc 패턴으로 변경해야함

@app.get("/")
async def home():
    return {"message" : "welcome to wanted_backend"}


@app.on_event("startup")
async def on_app_start():
	await db_manager.initiate_database()

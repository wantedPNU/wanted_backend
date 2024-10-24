from fastapi import FastAPI
# from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api import setting,query, video,inference, query_message
# from config.config import initiate_database
from database import db_manager
# from controller.user_controller import UserController

from urllib.parse import quote
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(video.router)
app.include_router(setting.router)
app.include_router(query.router)
app.include_router(inference.router)
app.include_router(query_message.router)

## 전체적인 구조 mvc 패턴으로 변경해야함

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인을 허용합니다.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용합니다.
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용합니다.
)
class Item(BaseModel):
    name: str
    

@app.get("/")
async def home():
    return {"message" : "welcome to wanted_backend"}

@app.on_event("startup")
async def on_app_start():
	await db_manager.initiate_database()

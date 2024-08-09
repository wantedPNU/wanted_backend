from fastapi import File, UploadFile, APIRouter,Body
from models.video import Video
from crud.crud import *
from database import db_manager
import gridfs
from pymongo import MongoClient


router = APIRouter()

@router.post(
        "/video/meta",
        response_description="Video data added into the database",        
        tags = ["post video meta to db"],
)
async def add_video_meta_to_db(video: Video = Body(...)):
    new_video = await create_video_meta(video)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "video entered successfully",
        "data": new_video,
    }


# @router.post(
#         "/video/file",
#         response_description="Video data added into the database",        
#         tags = ["post video file to db"],
# )
# async def add_video_file_to_db(file: UploadFile):    
#     new_video_file = await create_video_file(file)            
#     return {
#         "status_code": 200,
#         "response_type": "success",
#         "description": "video file entered successfully",                
#     }    
@router.post(
        "/video/file",
        response_description="Video data added into the database",        
        tags = ["post video file to db"],
)
async def add_video_file_to_db(file: UploadFile = File()):   
    #gridFS코드 추가해야함(서버에 있음) 
    # MongoDB 클라이언트 연결
    
    client = MongoClient('mongodb://localhost:27017/')
    # 데이터베이스 선택
    db = client['wanted']

    # GridFS 인스턴스 생성
    fs = gridfs.GridFS(db)

    contents = await file.read()
    file_id = fs.put(contents, filename=file.filename)
    
    # new_video_file = await create_video_file(file)            
    return {
        "status_code": 200,
        "response_type": "success",
        "description": f"video file entered successfully{file_id}",                             
    }    

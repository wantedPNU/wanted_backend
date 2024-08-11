from fastapi import File, UploadFile, APIRouter,Body
from models.video import Video
from crud.crud import *
from database import db_manager
import gridfs
from pymongo import MongoClient
from api import inference_setting
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

@router.post(
        "/video/file",
        response_description="Video data added into the database",        
        tags = ["post video file to db"],
)
async def add_video_file_to_db(file: UploadFile = File()):   
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wanted']
    fs = gridfs.GridFS(db)
    contents = await file.read()
    file_id = fs.put(contents, filename=file.filename)
    inference_setting.update_file_id(file_id)
    print(file_id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": f"video file entered successfully{file_id}",                             
    }    

from fastapi import File, UploadFile, APIRouter,Body
from models.video import Video
from crud.crud import *

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
async def add_video_file_to_db(file: UploadFile = File(...)):
    new_video_file = await create_video_file(file)            
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "video file entered successfully",                
    }    


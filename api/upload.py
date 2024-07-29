from fastapi import File, UploadFile, APIRouter,Body,HTTPException
from fastapi.responses import PlainTextResponse,JSONResponse
from tempfile import NamedTemporaryFile
from yolo_world.get_inference import process_video
from models.video import Video,VideoFile
import os
from database.database import *
from scheme.video import Response


router = APIRouter()

@router.post(
        "/video",
        response_description="Video data added into the database",
        response_model=Response,
        tags = ["upload test to db"],
)
async def add_video_data(video: Video = Body(...)):
    new_video = await add_video(video)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "video entered successfully",
        "data": new_video,
    }


@router.post(
        "/video/test3",
        response_description="Video data added into the database",        
        tags = ["upload test to db"],
)
async def detect_faces_V1(file: UploadFile = File(...)):
    new_video_file = await add_video_file(file)        
    print("hello3")
    # return {
    #     "status_code": 200,
    #     "response_type": "success",
    #     "description": "video file entered successfully",        
    #     "data" : new_video_file
    # }
    return {
        "message": "succeeded"
    }    



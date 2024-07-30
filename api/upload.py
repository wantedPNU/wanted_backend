from fastapi import File, UploadFile, APIRouter,Body,HTTPException
from fastapi.responses import PlainTextResponse,JSONResponse
from tempfile import NamedTemporaryFile
# from yolo_world.get_inference import process_video
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







@router.post("/video/test1", response_class=JSONResponse, tags=["upload test without db 1"])
async def detect_faces_in_video(video_file: UploadFile):
    
    # contents = await video_file.read()
    print(type(video_file)) # <class 'starlette.datastructures.UploadFile'>
    # print(type(contents)) # <class 'bytes'>

    return ""


@router.post("/video/test2", tags = ["upload test without db 2"])
def detect_faces(file: UploadFile = File(...)):
    temp = NamedTemporaryFile(delete=False)
    try:
        try:
            contents = file.file.read()
            with temp as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        
        res = process_video(temp.name)  # Pass temp.name to VideoCapture()
    except Exception:
        return {"message": "There was an error processing the file"}
    finally:
        #temp.close()  # the `with` statement above takes care of closing the file
        os.remove(temp.name)
        
    return res


@router.get("/test1/", tags=["get test"])
async def read_users():
    return{"message" : "testing..."}


@router.post("/test2/", tags=["post test"])
async def write_something(msg : str):
    return {"HELLO" : "POST", "msg" : msg}


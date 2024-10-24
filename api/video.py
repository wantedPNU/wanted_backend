from fastapi import File, UploadFile, APIRouter,Body,Form
from typing import List
from models.video import Video
from crud.crud import *
from database import db_manager
import gridfs
from pymongo import MongoClient
from api import inference_setting
import os

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
#         "/video/test"

# )
# async
@router.get(
    "/video/list",
    tags=["get videolist from server"],
)
async def find_video_list() -> dict:
    # 아침에 수정한거

    # dir_name = "sample_test_backup"
    # files_and_dirs = os.listdir(f"./yolo_world/input_video/{dir_name}/")
    # file_names = [f for f in files_and_dirs if os.path.isfile(os.path.join(f"./yolo_world/input_video/{dir_name}/", f))] 
    files_and_dirs = os.listdir(f"./yolo_world/input_video/")
    file_names = [f for f in files_and_dirs if os.path.isfile(os.path.join(f"./yolo_world/input_video/", f))]    
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "query entered successfully",
        "type" : type(file_names).__name__,     
        "file_names" : file_names
    }

@router.delete(
        "/video/{filename}"
)
async def delete_video_file(filename: str):    
    # 아침에 수정한거
    # dir_name = "sample_test_backup"
    # folder_path = f"./yolo_world/input_video/{dir_name}/"
    folder_path = f"./yolo_world/input_video/"
    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        return f"File '{filename}' deleted successfully."
    else:
        return f"File '{filename}' not found."
    


@router.delete("/video/file")
async def delete_video_files(filenames: List[str]):    
    # 아침에 수정한거
    # dir_name = "sample_test_backup"
    # folder_path = f"./yolo_world/input_video/{dir_name}/"
    folder_path = f"./yolo_world/input_video/"
    deleted_files = []
    not_found_files = []

    for filename in filenames:
        file_path = os.path.join(folder_path, filename)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            deleted_files.append(filename)
        else:
            not_found_files.append(filename)

    return {
        "deleted": deleted_files,
        "not_found": not_found_files
    }

@router.post(
        "/video/file",
        response_description="Video data added into the database",        
        tags = ["post video file to db"],
)
async def add_video_file_to_db(location: str = Form(...), file: UploadFile = File()):   
        
    file_id = await create_video_to_db(location, file)
    
    return {
        "status_code": 200,
        "response_type": "success",
        "description": f"video file entered successfully{file_id}",                             
    }    

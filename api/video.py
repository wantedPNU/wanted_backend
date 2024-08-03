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


@router.get(
    "/video/file",
    response_description="get Video data from the database",
    tags = ["get video file from db"],
)
async def get_video_file_from_db(videoid: str):
    video = await read_video(videoid)
    # print(video['file_data'])
    print(type(video['file_data']))
    
    video_bytes = video['file_data']    
    output_file_path = 'output_video.mp4'
    
    with open(output_file_path, 'wb') as video_file:
        video_file.write(video_bytes)

    print(f"비디오 파일이 {output_file_path}에 저장되었습니다.")
    return {
        "status_code": 200,
        "response_type": "success",        
    }

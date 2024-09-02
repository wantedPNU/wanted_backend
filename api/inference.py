from fastapi import APIRouter,Body,HTTPException
from models.video import Video
from crud.crud import *
import os
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
import gridfs
from pymongo import MongoClient
from api import inference_setting
from yolo_world import progress_value
from yolo_world import prevWorld,curWorld
from io import BytesIO
import zipfile
import asyncio
from yolo_world.curWorld import progress_test
router = APIRouter()

IMAGE_DIRECTORY = "./frames/"


async def generate_numbers():
    # num = get_progress_value()
    # progress_value.update_progress_son(0)
    while True:        
        value = progress_value.get_progress_value()
        print(value)
        yield f"data: {value}\n\n"        
        # if(progress_done()): ## progress_done으로 바꿔야함.
        # num += 1
        if progress_value.get_progress_value() == 1:
            break;        
        await asyncio.sleep(0.5)  # 1초마다 숫자를 전송


@router.get(
    "/inference/progress"
)
async def sse_test():
    print("start sse")        
    return StreamingResponse(generate_numbers(), media_type="text/event-stream")


@router.get(
    "/inference",
    response_description="get inference data from server",
    tags = ["get inference data from server"],
)
async def get_inference_result_from_server(scoreThreshold: float , frameInterval : int):
    os.system("rm -rf ./frames")
    os.system("rm -rf ./custom_yolov8s.pt")

    print(scoreThreshold)
    print(frameInterval)
    inference_setting.update_settings(scoreThreshold, frameInterval)
    progress_value.update_progress_son(0)
    print("starting yoloworld...")
    
    # yoloworld 모델 시작    
    curWorld.run_inference(inference_setting)
    
    frames_directory = os.path.join("./", "frames")
    if not os.path.exists(frames_directory):
        raise HTTPException(status_code=404, detail="Frames directory not found")

    image_filenames = [f for f in os.listdir(frames_directory) if f.endswith(('결과.jpg'))]
    if not image_filenames:
        raise HTTPException(status_code=404, detail="No images found in frames directory")

    def iter_file():
        with BytesIO() as zip_buffer:
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for image_filename in image_filenames:
                    image_path = os.path.join(frames_directory, image_filename)
                    zip_file.write(image_path, image_filename)
            zip_buffer.seek(0)
            yield from zip_buffer  # Yield the content in chunks

    return StreamingResponse(iter_file(), media_type="application/zip")
    # 이거는 왜 안되는지 조사
    # test = FileResponse(image_path,media_type='image/jpeg')  
    # print(test.media_type)
    # print(test.body)

    # return {
    #     test
    # }
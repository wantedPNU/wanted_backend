from fastapi import APIRouter,HTTPException
from crud.crud import *
import os
from starlette.responses import StreamingResponse
from api import inference_setting
from yolo_world import progress_value
from yolo_world import prevWorld,curWorld
from io import BytesIO
import zipfile
import asyncio
# from yolo_world.curWorld import progress_test

import time
import threading 


IMAGE_DIRECTORY = "./frames/"

router = APIRouter()

async def generate_numbers():    
    num = 0
    print("generate numbers 시작")
    while True:                
        yield f"data: {num}\n\n"                
        num += 1
        print(num)
        # print("----------------------------------------------------------------------------------------------------")
        if num == 10:
            break
        await asyncio.sleep(1)  # 1초마다 숫자를 전송


async def generate_numbers_str():    
    str = "str"
    num = 0
    print("generate numbers str 시작")
    while True:                
        yield f"message: {str}\n\n"                
        num += 0.5
        print(str)
        print(num)        
        if num == 10:
            break
        await asyncio.sleep(0.5)  # 1초마다 숫자를 전송


def generate_numbers_without_async():    
    num = 0
    print("generate numbers without async 시작")
    while True:                
        yield f"data: {num}\n\n"                
        num += 1
        print(num)        
        if num == 10:
            break
        time.sleep(1)  # 1초마다 숫자를 전송

async def generate_progress_value():
    value = 0 
    num = 0   
    while True:
        # value = progress_value.get_progress_value()        
        # yield f"data: {value}\n\n"
        yield f"data: {num}\n\n"
        num += 1
        if(value == 1):
            break
        await asyncio.sleep(1)
        


@router.get(
        "/async/test"
)
async def async_test():  
    # asyncio.create_task(generate_numbers_str())    
    return StreamingResponse(generate_numbers_str(),media_type="text/event-stream")


# @router.get(
#     "/inference/progress"
# )
# async def sse_test():
#     # print("start sse")  
#     # thread_1 = threading.Thread(target = generate_numbers)   
#     # thread_1.start()         
#     return StreamingResponse(generate_numbers(), media_type="text/event-stream")


@router.get(
    "/inference/progress"
)
async def sse_test():
    # print("start sse")  
    # thread_1 = threading.Thread(target = generate_numbers)   
    # thread_1.start()         
    return StreamingResponse(generate_progress_value(), media_type="text/event-stream")

@router.get(
    "/inference",
    response_description="get inference data from server",
    tags = ["get inference data from server"],
)
async def get_inference_result_from_server(scoreThreshold: float , frameInterval : int):
    os.system("rm -rf ./frames")    
    
    inference_setting.update_settings(scoreThreshold, frameInterval)
    progress_value.update_progress_son(0)    

    print("starting yoloworld...")    

    # yoloworld 모델 시작    
    await curWorld.run_inference(inference_setting)
    
    # asyncio.sleep(3)


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



# @router.get(
#     "/inference/preview",        
# )
# async def get_inference_preview_from_server(scoreThreshold: float , frameInterval : int):
    
#     frames_directory = os.path.join("./", "frames")
#     if not os.path.exists(frames_directory):
#         raise HTTPException(status_code=404, detail="Frames directory not found")

#     image_filenames = [f for f in os.listdir(frames_directory) if f.endswith(('결과.jpg'))]
#     if not image_filenames:
#         raise HTTPException(status_code=404, detail="No images found in frames directory")
    
#     def iter_file():
#         with BytesIO() as zip_buffer:
#             with zipfile.ZipFile(zip_buffer, "w") as zip_file:
#                 for image_filename in image_filenames:
#                     image_path = os.path.join(frames_directory, image_filename)
#                     zip_file.write(image_path, image_filename)
#             zip_buffer.seek(0)
#             yield from zip_buffer  # Yield the content in chunks

#     return StreamingResponse(iter_file(), media_type="application/zip")    


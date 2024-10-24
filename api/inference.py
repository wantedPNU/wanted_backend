from fastapi import APIRouter,HTTPException
from fastapi.responses import FileResponse
from crud.crud import *
import os
from starlette.responses import StreamingResponse
from api import inference_setting
from yolo_world import progress_value,detected_video_list
from io import BytesIO
from typing import List, Dict
import zipfile
import re

from yolo_world import curWorld 


IMAGE_DIRECTORY = "./frames/"

router = APIRouter()



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

    frames_directory = os.path.join("./", "frames")
    if not os.path.exists(frames_directory):
        raise HTTPException(status_code=404, detail="Frames directory not found")

    pattern = re.compile(r'.*결과\d+\.jpg$')
    
    image_filenames = [f for f in os.listdir(frames_directory) if pattern.match(f)]
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

@router.get("/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join("./frames", filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)


@router.get("/high-probablity-locations", response_model = List[Dict[str, str]])
async def get_high_probablity_locations():
    frames_directory = "./frames"
    if not os.path.exists(frames_directory):
        raise HTTPException(status_code=404, detail="Frames directory not found")

    pattern = re.compile(r'.*결과\d+\.jpg$')

    image_filenames = [f for f in os.listdir(frames_directory) if pattern.match(f)]
    if not image_filenames:
        raise HTTPException(status_code=404, detail="No images found in frames directory")
    
    location_list = []
    #filename으로 video 이름을 찾고, 

    
    for image_filename in image_filenames:
        print(image_filenames)
        video_name = detected_video_list.get_video(image_filename)
        location_data = await get_location_from_video(video_name)
        print(location_data.get('location'))
        location_list.append({
            "filename":image_filename,
            "location" : location_data.get('location')
        })            
    
    if not location_list:
        raise HTTPException(status_code=404, detail="No locations found for the provide images")
    
    return location_list

@router.get("/high-probability-images", response_model=List[Dict[str, str]])
async def get_high_probability_images():
    frames_directory = "./frames"
    if not os.path.exists(frames_directory):
        raise HTTPException(status_code=404, detail="Frames directory not found")

    pattern = re.compile(r'.*결과\d+\.jpg$')

    image_filenames = [f for f in os.listdir(frames_directory) if pattern.match(f)]
    if not image_filenames:
        raise HTTPException(status_code=404, detail="No images found in frames directory")

    
    location_list = []

    for image_filename in image_filenames:

        video_name = detected_video_list.get_video(image_filename)        
        
        location_data = await get_location_from_video(video_name)        
        
        location_list.append({
            "filename":image_filename,
            "url" : location_data.get('location')
        })           

    return location_list
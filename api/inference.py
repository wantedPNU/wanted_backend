from fastapi import APIRouter,Body,HTTPException
from models.video import Video
from crud.crud import *
import os
from fastapi.responses import FileResponse

router = APIRouter()

IMAGE_DIRECTORY = "./frames/"
@router.get(
    "/inference",
    response_description="get inference data from server",
    tags = ["get inference data from server"],
)
async def get_inference_result_from_server():  
    print("starting yoloworld...")
    os.system("python yolo_world/prevWorld.py")

    image_path = os.path.join(IMAGE_DIRECTORY, "1_res.jpg")
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return {
        FileResponse(image_path)  
    }

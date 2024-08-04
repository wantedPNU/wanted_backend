from fastapi import APIRouter,Body
from models.video import Video
from crud.crud import *
import os

router = APIRouter()


@router.get(
    "/inference",
    response_description="get inference data from server",
    tags = ["get inference data from server"],
)
async def get_inference_result_from_server():  
    print("helloworld")   
    os.system("python yolo_world/prevWorld.py")

    return {
        "status_code": 200,
        "response_type": "success",        
    }

from fastapi import APIRouter,Body,HTTPException
from models.video import Video
from crud.crud import *
import os
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
import gridfs
from pymongo import MongoClient
from api import inference_setting
from yolo_world import prevWorld
from io import BytesIO
import zipfile

router = APIRouter()

IMAGE_DIRECTORY = "./frames/"
@router.get(
    "/inference",
    response_description="get inference data from server",
    tags = ["get inference data from server"],
)
async def get_inference_result_from_server(scoreThreshold: float , frameInterval : int):
    os.system("rm -rf ./frames")
    os.system("rm -rf ./input_video.mp4")
    print(scoreThreshold)
    print(frameInterval)
    inference_setting.update_settings(scoreThreshold, frameInterval)
    # client = MongoClient('mongodb://localhost:27017/')
    # db = client['wanted']
    # fs = gridfs.GridFS(db)
    # file_id = ObjectId(inference_setting.file_id)
    # output_path = 'input_video.mp4'

    # with open(output_path, 'wb') as f:
    #     f.write(fs.get(file_id).read())

    # print(f"비디오 파일이 {output_path}에 저장되었습니다. 저장한 비디오 파일을 기반으로 추론을 시작합니다.")
    
    print("starting yoloworld...")
    
    # yoloworld 모델 시작    
    prevWorld.run_inference(inference_setting)
    
    frames_directory = os.path.join("./", "frames")
    if not os.path.exists(frames_directory):
        raise HTTPException(status_code=404, detail="Frames directory not found")

    image_filenames = [f for f in os.listdir(frames_directory) if f.endswith(('_res.jpg'))]
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
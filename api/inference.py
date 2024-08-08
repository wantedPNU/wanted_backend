from fastapi import APIRouter,Body,HTTPException
from models.video import Video
from crud.crud import *
import os
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
router = APIRouter()

IMAGE_DIRECTORY = "./frames/"
@router.get(
    "/inference",
    response_description="get inference data from server",
    tags = ["get inference data from server"],
)
async def get_inference_result_from_server():  
    #추론하고 싶은 비디오의 db상의 id
    videoid = "66add2b4a5a86d238117a3fb"
    video = await read_video(videoid)  
    #넣고 싶은 쿼리의 db상의 id
    queryid = "66a9e5b7a8fdec6af6edd5e3"      
    query = await read_query(queryid)

    video_bytes = video['file_data']    
    input_file_path = 'input_video.mp4'
    
    with open(input_file_path, 'wb') as video_file:
        video_file.write(video_bytes)

    print(f"비디오 파일이 {input_file_path}에 저장되었습니다. 저장한 비디오 파일을 기반으로 추론을 시작합니다.")
    

    print("starting yoloworld...")
    # yoloworld 모델 시작
    # os.system("python yolo_world/prevWorld.py")

    #추론 결과 이미지 이름을 "3_res.jpg" 대신에 넣으면됨. 
    image_path = os.path.join(IMAGE_DIRECTORY, "1_res.jpg")
    print(image_path)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    

    return StreamingResponse(open(image_path, mode="rb"), media_type='image/jpeg')
    
    # 이거는 왜 안되는지 조사
    # test = FileResponse(image_path,media_type='image/jpeg')  
    # print(test.media_type)
    # print(test.body)

    # return {
    #     test
    # }

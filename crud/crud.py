
import os
from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import File
from models.video import Video,VideoFile,VideoLocation
from models.query import Query
from database import db_manager
from pymongo import MongoClient
import gridfs

async def create_query(new_query: Query) -> Query:    
    query = await new_query.create()
    return query

async def read_query(queryid: str)->Query:
    query = await db_manager.db.Query.find_one({"_id" :ObjectId(queryid)})    
    return query

async def read_video(videoid: str)->VideoFile:
    video = await db_manager.db.VideoFile.find_one({"_id" : ObjectId(videoid)})
    return video


async def create_video_meta(new_video: Video) -> Video:    
    video = await new_video.create()
    return video

async def get_location_from_video(video_name : str):
    
     # MongoDB 클라이언트 설정
    client = MongoClient('mongodb://localhost:27017/')
    db = client['wanted']
    collection = db['meta']  # 'meta' collection 선택
        
    # video_name으로 location 찾기
    location_data = collection.find_one({"video_name": video_name})

    if location_data:
        return location_data
    else:
        return None  # 해당 비디오 이름이 없을 경우 None 반환

#todo
#같은 비디오 이름으로 다른 위치가 들어 왔을때 수정하는 것(or 삭제후 추가, 전체적으로 update 에 대한 기능이 없음)

async def create_video_to_db(_location: str, file= File()):        
    client = MongoClient('mongodb://localhost:27017/')        
    # client = db_manager.client
    db = client['wanted']    
    collection = db["meta"]
    # db = db_manager.db
    fs= gridfs.GridFS(db)    
    
    
    meta = db.meta
    location = {
        "location" : _location,
        "video_name" : file.filename
    }
    meta.insert_one(location)
    contents = await file.read()

    #save file to db
    filename_without_extension = os.path.splitext(file.filename)[0]
    file_id = fs.put(contents, filename=filename_without_extension)

    # #why??
    # inference_setting.update_file_id(file_id)          
    # file_id = ObjectId(inference_setting.file_id)
    
    #save file 
    # 아침에 수정한거
    # dir_name = "sample_test_backup"
    # files_and_dirs = os.listdir(f"./yolo_world/input_video/{dir_name}/")
    # file_names = [f for f in files_and_dirs if os.path.isfile(os.path.join(f"./yolo_world/input_video/{dir_name}/", f))]
    files_and_dirs = os.listdir(f"./yolo_world/input_video/")
    file_names = [f for f in files_and_dirs if os.path.isfile(os.path.join(f"./yolo_world/input_video/", f))]
    
    #todo : reject input if it is same video
    # output_path = f'./yolo_world/input_video/{dir_name}/{file.filename}'
    output_path = f'./yolo_world/input_video/{file.filename}'
    
    with open(output_path, 'wb') as f:
        f.write(fs.get(file_id).read())
        
    print(f"비디오 파일이 {output_path}에 저장되었습니다.")

    return file_id





#  현재 미상용(gridfs 사용중)
# async def create_video_file(file):
#     # video_file = await new_video_file.create()
#     # return video_file
#     # try:
    
#     file_data = await file.read()    
#     # file_data = file
#     video_file = VideoFile(
#         # filename=file.filename,
#         # content_type=file.content_type,
#         file_data=file_data
#     )
#     await video_file.insert()
#     return video_file
#     # except Exception as e:
#     #     raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

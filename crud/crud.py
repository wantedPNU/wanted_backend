
import os
from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import File
from models.video import Video,VideoFile
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


async def create_video_to_db(location: str, file= File()):    
    
    client = MongoClient('mongodb://localhost:27017/')        
    # client = db_manager.client
    db = client['wanted']    
    # db = db_manager.db
    fs= gridfs.GridFS(db)

    print(location)
    
    contents = await file.read()

    #save file to db
    file_id = fs.put(contents, filename=file.filename)

    # #why??
    # inference_setting.update_file_id(file_id)          
    # file_id = ObjectId(inference_setting.file_id)
    
    #save file 
    files_and_dirs = os.listdir("./yolo_world/input_video/samples/")
    file_names = [f for f in files_and_dirs if os.path.isfile(os.path.join("./yolo_world/input_video/samples/", f))]
    
    #todo : reject input if it is same video
    output_path = f'./yolo_world/input_video/samples/{file.filename}.mp4'
    
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

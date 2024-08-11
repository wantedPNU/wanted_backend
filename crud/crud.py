
from beanie import PydanticObjectId
from bson import ObjectId
from models.video import Video,VideoFile
from models.query import Query
from database import db_manager


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

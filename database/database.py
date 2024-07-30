
from beanie import PydanticObjectId

from models.video import Video,VideoFile
from models.admin import Query
from fastapi import File,HTTPException


async def add_query(new_query: Query) -> Query:
    query = await new_query.create()
    return query


async def add_video(new_video: Video) -> Video:
    video = await new_video.create()
    return video


async def add_video_file(file):
    # video_file = await new_video_file.create()
    # return video_file
    # try:
    file_data = await file.read()
    print(file_data)

    video_file = VideoFile(
        # filename=file.filename,
        # content_type=file.content_type,
        file_data=file_data
    )
    print("hello")
    await video_file.insert()
    print("hello2")
    return video_file
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

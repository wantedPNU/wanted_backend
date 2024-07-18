from beanie import PydanticObjectId

from models.video import Video

video_collection = Video


async def add_video(new_video: Video) -> Video:
    video = await new_video.create()
    return video



@router.post(
        "/video",
        response_description="Video data added into the database",
        response_model=Response,
        tags = ["upload test to db"],
)
async def add_video_data(video: Video = Body(...)):
    new_video = await add_video(video)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "video entered successfully",
        "data": new_video,
    }

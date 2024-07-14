from fastapi import APIRouter, Body, Depends, HTTPException, status

router = APIRouter()


@app.post("/set_search_settings")
async def set_search_settings(video_id: str, settings: SearchSettings):
    if video_id not in videos:
        raise HTTPException(status_code=404, detail="Video not found")

    search_settings[video_id] = settings.dict()
    return JSONResponse(status_code=204)

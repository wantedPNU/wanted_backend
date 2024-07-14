from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid

app = FastAPI()


class Description(BaseModel):
    description: str

class SearchSettings(BaseModel):
    scorethreshold: float
    frameinterval: int

@app.post("/set_description")
async def set_description(video_id: str, description: Description):
    if video_id not in videos:
        raise HTTPException(status_code=404, detail="Video not found")

    descriptions[video_id] = description.description
    return JSONResponse(status_code=204)

@app.get("/search_results")
async def search_results(video_id: str = Query(...)):
    if video_id not in videos:
        raise HTTPException(status_code=404, detail="Video not found")

    # 여기에 실제 검색 로직 구현 필요
    results = [
        {"start_time": "00:01:23", "end_time": "00:01:30"},
        {"start_time": "00:05:10", "end_time": "00:05:15"},
    ]
    return {"status": "search completed", "results": results}

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

class SearchSettings(BaseModel):
    score_threshold: float
    frame_interval: int

router = APIRouter()

@router.post("/search-setting",
             status_code=201,
             response_description="parametere set",
             responses = {
                400: {"description": "Wrong Parameter"},
            },
             tags=["Setting parameter"])
async def update_search_settings(settings: SearchSettings):
    if settings.score_threshold < 0 or settings.score_threshold > 1 or \
       settings.frame_interval < 1 or settings.frame_interval > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST\
                            , detail="Wrong Parameter")
    try:
        # 설정 업데이트
        return {"status": "search settings updated"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR\
                            , detail="Internal Server Error")
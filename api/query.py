from fastapi import File, UploadFile, APIRouter,Body,HTTPException
from fastapi.responses import PlainTextResponse,JSONResponse
from tempfile import NamedTemporaryFile
from models.video import Video,VideoFile
from database.database import *
from scheme.video import Response
from models.admin import Query,TextOutput
from pymongo.errors import PyMongoError

router = APIRouter()

@router.post("/process-text", response_model=TextOutput)
async def process_text(query: Query):
    # 입력된 텍스트 가져오기
    input_text = query.text

    # 단어 목록 생성
    words = input_text.split()

    # 각 단어를 MongoDB에 저장
    for word in words:
        try:
            # 단어가 이미 있는지 확인하고 없으면 삽입
            # word_collection.update_one(
            #     {"word": word},
            #     {"$set": {"word": word}},
            #     upsert=True
            # )
            new_query = add_query(query)

        except PyMongoError as e:
            # 예외 발생 시 사용자에게 알림
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # 응답 데이터 준비
    # return TextOutput(
    #     words=words,
    #     word_count=len(words)
    # )

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "video entered successfully",
        "data": new_query,
    }

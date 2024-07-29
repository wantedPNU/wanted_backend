from fastapi import File, UploadFile, APIRouter,Body,HTTPException
from fastapi.responses import PlainTextResponse,JSONResponse
from tempfile import NamedTemporaryFile
from yolo_world.get_inference import process_video
from models.video import Video,VideoFile
import os
from database.database import *
from scheme.video import Response


router = APIRouter()

@router.post("/process-text", response_model=TextOutput)
async def process_text(input_data: TextInput):
    # 입력된 텍스트 가져오기
    input_text = input_data.text

    # 단어 목록 생성
    words = input_text.split()

    # 각 단어를 MongoDB에 저장
    for word in words:
        try:
            # 단어가 이미 있는지 확인하고 없으면 삽입
            word_collection.update_one(
                {"word": word},
                {"$set": {"word": word}},
                upsert=True
            )
        except PyMongoError as e:
            # 예외 발생 시 사용자에게 알림
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # 응답 데이터 준비
    return TextOutput(
        words=words,
        word_count=len(words)
    )

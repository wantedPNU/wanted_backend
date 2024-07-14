from fastapi import APIRouter, Body, Depends, HTTPException, status

router = APIRouter()


@app.post("/uploadvideo")
async def upload_video(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    video_id = str(uuid.uuid4())
    videos[video_id] = file.filename  # 여기서는 파일명을 저장, 실제로는 파일을 저장소에 저장 필요
    return {"video_id": video_id}


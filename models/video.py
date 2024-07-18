from beanie import Document
from fastapi import Form #동영상 처리 자료형

class Video(Document):
    name : str
    length : int
    class Config:
        json_schema_extra = {
            "example": {
                "name": "cctv in vb lab",
                "length": 5,
            }
        }
    
    class Settings:
        name = "video"


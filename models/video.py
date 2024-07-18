from beanie import Document

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


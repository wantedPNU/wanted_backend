from typing import Optional
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

class VideoFile(Document):
    # name : str    
    # content_type : str
    file_data : Optional[bytes]

    class Config:
        json_schema_extra = {
            "example": {
                # "name" : "example video",
                # "content_type" : "video/mp4",
                "file_data" : "b'file binary data'"
            }
        }

    
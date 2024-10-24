from beanie import Document
from pydantic import BaseModel

class Query(Document):
    text: str
    class Config:
        json_schema_extra = {
            "example": {
                "text": "woman with blue shirt, man with white shirt",
            }
        }    


class TextOutput(BaseModel):
    words: list[str]
    word_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "words": ["woman","man"],
                "word_count" : 2,
            }
        }
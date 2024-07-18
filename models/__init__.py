# motor - MongoDB 용 비동기 python 라이브러리
from models.admin import Admin
from models.video import Video
# from odmantic import AIOEngine

__all__ = [Video,Admin]
#secrets.json 가져오기
# from config import MONGO_DB_NAME, MONGO_DB_URL
# from pymongo import MongoClient

# class MongoDB:
#     def __init__(self):
#         self.client = None
#         self.engine = None

#     def connect(self):
#         self.client = AsyncIOMotorClient(MONGO_DB_URL)
#         self.engine = AIOEngine(client=self.client, database=MONGO_DB_NAME)
#         print("DB 와 연결되었습니다.")
       
    
#     def close(self):
#         self.client.close()

# mongodb = MongoDB()
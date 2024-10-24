from fastapi import APIRouter,Body
from crud.crud import *
from models.query import Query
from yolo_world import prevWorld
from api import inference_setting

router = APIRouter()
@router.post(
        "/query",        
        tags = ["post query to db"]
)
async def save_query(queryString:str= Body(...)):      
    print(queryString)
    query = Query(text=queryString)
    query.text = queryString
    inference_setting.update_query(query.text[10:-2].split(','), False)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "query saved successfully",        
    }

@router.post(
        "/query/test",        
        tags = ["post query to db which doesn't works well"]
)
async def save_query(query:Query= Body(...)):                  
    new_query = await create_query(query)    
    print(new_query.text)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "query entered successfully",        
    }


@router.get(
    "/query",
    tags=["get query from db"],
)
async def find_query(queryid: str) -> dict:
    query = await read_query(queryid)
    print(query['text'])
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "query entered successfully",
        "type" : type(query).__name__,       
        "query text" : query['text'],
    }



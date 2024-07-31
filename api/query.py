from fastapi import APIRouter,Body
from crud.crud import *
from models.query import Query


router = APIRouter()

@router.post(
        "/query",        
        tags = ["post query to db"]
)
async def save_query(query: Query = Body(...)):      
    new_query = await create_query(query)
    print(new_query.text)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "query entered successfully",
        "data": new_query,
    }


@router.get(
    "/query",
    tags=["get query from db"],
)
async def find_query(queryid: str) -> Query:
    query = await read_query(queryid)
    print(query.text)
    return {
        "queryText" : query.text
    }



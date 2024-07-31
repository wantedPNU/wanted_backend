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
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "query entered successfully",
        "data": new_query,
    }


# @router.get(
#     "/query",
#     taggs=["get query from db"]
# )
# async def find_query():
#     query = await read_query()



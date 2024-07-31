from fastapi import APIRouter,Body
from database.database import *
from models.query import Query


router = APIRouter()

@router.post(
        "/query",        
        tags = ["post query to db"]
)
async def process_query(query: Query = Body(...)):      
    new_query = await add_query(query)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "query entered successfully",
        "data": new_query,
    }



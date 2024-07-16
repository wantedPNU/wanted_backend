from fastapi import APIRouter

router = APIRouter()


@router.get("/test1/", tags=["get test"])
async def read_users():
    return "helloworfff"

@router.post("/test2/", tags=["post test"])
async def write_something(msg : str):
    return {"HELLO" : "POST", "msg" : msg}


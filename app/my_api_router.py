from fastapi import APIRouter, Request
from fastapi.responses import  JSONResponse

router = APIRouter()

@router.post("/create_internal_server_error")
async def create_internal_server_error(request:Request):
    request.app.logger.info("[]")
    request.app.logger.error("Internal server error no ")
    data = {"status": False,
            "message": "Internal Server Error",
            "data": None}
    return JSONResponse(status_code=500,
                        content=data)

@router.get("/create_valid_request")
async def create_valid_request(request:Request):
    data = {"status": True,
            "message": "data found",
            "data": {
                "name": "karan",
                "age": 21,
            }}
    return JSONResponse(status_code=200,
                        content=data)

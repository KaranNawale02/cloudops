from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

# In-memory database
temp_Db = {}

# Pydantic model
class User(BaseModel):
    name: str
    id: int


# 1. Simulated Internal Server Error
@router.post("/create-internal-server-error")
async def create_internal_server_error(request: Request):
    request.app.logger.info("[CREATE_INTERNAL_SERVER_ERROR] Triggered")
    try:
        raise ValueError("Simulated error")

    except Exception as e:
        request.app.logger.error(f"[CREATE_INTERNAL_SERVER_ERROR] Internal server error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": False,
                "message": "Internal Server Error",
                "data": None,
            },
        )


# 2. Create User
@router.post("/create-user")
async def create_user(request: Request, user: User):
    try:
        if user.id in temp_Db:
            return JSONResponse(
                status_code=400,
                content={"status": False, "message": "User already exists", "data": None},
            )

        temp_Db[user.id] = user.dict()
        request.app.logger.info(f"[CREATE_USER] User {user.id} inserted successfully!")
        return JSONResponse(
            status_code=201,
            content={"status": True, "message": "User Added", "data": user.dict()},
        )
    except Exception as e:
        request.app.logger.error(f"[CREATE_USER] Internal server error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "Internal Server Error", "data": None},
        )


# 3. Update User
@router.put("/update-user")
async def update_user(request: Request, user: User):
    try:
        if user.id not in temp_Db:
            return JSONResponse(
                status_code=404,
                content={"status": False, "message": "User not found", "data": None},
            )

        temp_Db[user.id] = user.dict()
        request.app.logger.info(f"[UPDATE_USER] User {user.id} updated successfully!")
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "User Updated", "data": user.dict()},
        )
    except Exception as e:
        request.app.logger.error(f"[UPDATE_USER] Internal server error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "Internal Server Error", "data": None},
        )


# 4. Delete User
@router.delete("/delete-user/{user_id}")
async def delete_user(request: Request, user_id: int):
    try:
        if user_id not in temp_Db:
            return JSONResponse(
                status_code=404,
                content={"status": False, "message": "User not found", "data": None},
            )

        del temp_Db[user_id]
        request.app.logger.info(f"[DELETE_USER] User {user_id} deleted successfully!")
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "User Deleted", "data": {"user_id": user_id}},
        )
    except Exception as e:
        request.app.logger.error(f"[DELETE_USER] Internal server error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "Internal Server Error", "data": None},
        )


# 5. Get All Users
@router.get("/all-users")
async def get_all_users(request: Request):
    try:
        request.app.logger.info(f"[GET_ALL_USERS] {len(temp_Db)} users found")
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "Data found", "data": temp_Db},
        )
    except Exception as e:
        request.app.logger.error(f"[GET_ALL_USERS] Internal server error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "Internal Server Error", "data": None},
        )

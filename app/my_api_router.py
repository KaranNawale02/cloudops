from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from psycopg.rows import dict_row

router = APIRouter()

# In-memory database
temp_Db = {}

# Pydantic model
class User(BaseModel):
    first_name:str
    last_name: str
    email: str
    contact_number: str


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
        query = """
            INSERT INTO public.user_accounts(first_name, last_name, contactemail, contactnumber)
            VALUES (%s, %s, %s, %s)
            RETURNING first_name,last_name;
        """
        values = (user.first_name, user.last_name, user.email, user.contact_number)

        async with request.app.db_conn.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(query, values)
                result = await cur.fetchone()

        if result:
            request.app.logger.info(f"[CREATE_USER] User {result['first_name']} inserted successfully!")
            return JSONResponse(
                status_code=201,
                content={"status": True, "message": "User Added", "data": result},
            )

        request.app.logger.warning("[CREATE_USER] User not created!")
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "User not created"}
        )

    except Exception as e:
        request.app.logger.error(f"[CREATE_USER] Internal server error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "Internal Server Error", "data": None},
        )


# 3. Update User
@router.put("/update-user/{user_id}")
async def update_user(request: Request, user_id: str , user: User):
    try:
        query = """
            UPDATE public.user_accounts
            SET first_name = %s,
                last_name = %s,
                contactemail = %s,
                contactnumber = %s
            WHERE id = %s::uuid
            RETURNING first_name,last_name;
        """
        values = (
            user.first_name,
            user.last_name,
            user.email,
            user.contact_number,
            user_id,
        )

        async with request.app.db_conn.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(query, values)
                result = await cur.fetchone()

        if result:
            request.app.logger.info(f"[UPDATE_USER] User {user_id} updated successfully!")
            return JSONResponse(
                status_code=200,
                content={"status": True, "message": "User Updated", "data": result},
            )

        return JSONResponse(
            status_code=404,
            content={"status": False, "message": "User not found", "data": None},
        )

    except Exception as e:
        request.app.logger.error(f"[UPDATE_USER] Internal server error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "Internal Server Error", "data": None},
        )



# 4. Delete User
@router.delete("/delete-user/{user_id}")
async def delete_user(request: Request, user_id: str):
    try:
        query = "DELETE FROM public.user_accounts WHERE id = %s RETURNING id;"

        async with request.app.db_conn.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(query, (user_id,))
                result = await cur.fetchone()

        if result:
            request.app.logger.info(f"[DELETE_USER] User {user_id} deleted successfully!")
            return JSONResponse(
                status_code=200,
                content={"status": True, "message": "User Deleted", "data": {"user_id": user_id}},
            )

        return JSONResponse(
            status_code=404,
            content={"status": False, "message": "User not found", "data": None},
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
        query = "SELECT id::text, first_name, last_name, contactemail AS Email, contactnumber FROM public.user_accounts ORDER BY created_at DESC;"

        async with request.app.db_conn.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(query)
                results = await cur.fetchall()

        request.app.logger.info(f"[GET_ALL_USERS] {len(results)} users found")
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "Data found", "data": results},
        )

    except Exception as e:
        request.app.logger.error(f"[GET_ALL_USERS] Internal server error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "Internal Server Error", "data": None},
        )


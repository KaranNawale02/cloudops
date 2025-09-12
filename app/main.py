from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request
from my_api_router import router
from project_logger import LogConfig
import logging
import psycopg2
import psycopg_pool

conn_string = 'postgresql://admin:admin@192.168.2.56:5432/postgres'

class DBConnectionPool:
    def __init__(self):
        self.psyco_async_pool: psycopg_pool.AsyncConnectionPool = psycopg_pool.AsyncConnectionPool(
            conn_string,
            min_size=1,
            max_size=5,
            open=False
        )

    async def close(self):
        await self.psyco_async_pool.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setting up application logger
    LogConfig.setup_logging()
    app.logger = logging.getLogger("beacon")

    # DB connection here
    app.db_conn = DBConnectionPool()
    await app.db_conn.psyco_async_pool.open()
    yield

    # DB connection closed
    await app.db_conn.close()


app = FastAPI(lifespan=lifespan,
              debug=True,
              title="Beacon")

app.include_router(router=router,tags=["Router"])


@app.get("/")
async def root_path(request:Request):
    request.app.logger.info("Hello From Root")
    return {"message":"Hello World !"}

if __name__ == "__main__":
    uvicorn.run(app=app,host='0.0.0.0',port=8000)
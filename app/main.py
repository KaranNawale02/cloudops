from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request
from my_api_router import router
from project_logger import LogConfig
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setting up application logger
    LogConfig.setup_logging()
    app.logger = logging.getLogger("backend")

    # DB connection here
    app.db_connection = "This is db connection"
    yield

    # DB connection closed
    app.db_connection = None


app = FastAPI(lifespan=lifespan,
              debug=True,
              title="MyProject")

app.include_router(router=router,tags=["Router"])


@app.get("/")
async def root_path(request:Request):
    request.app.logger.info("Hello From Root")
    return {"message":"Hello World !"}

if __name__ == "__main__":
    uvicorn.run(app=app,host='0.0.0.0',port=8000)
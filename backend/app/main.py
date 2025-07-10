import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import *
from app.services import encoder, qdrant
from app.config import settings

from contextlib import asynccontextmanager
from .config import setup_logging
import logging
from app.services import database

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await encoder.initialize()
    print("Connecting to qdrant", flush=True)
    qdrant.initialize(settings.qdrant_host, settings.qdrant_port)
    database.Base.metadata.create_all(database.engine)
    # await qdrant.loadCourses()
    # app.state.courses_load_task = asyncio.create_task(qdrant.loadCourses())
    yield
    # Clean up the ML models and release the resources


app = FastAPI(
    docs_url="/api/swagger",  # вместо /docs
    redoc_url="/api/redocly",  # вместо /redoc
    openapi_url="/api/schema",  # вместо /openapi.json
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(chats.router)
app.include_router(courses.router)


logger.info("Application started")


@app.get("/")
async def root():
    return {"message": "Hello Universe!"}

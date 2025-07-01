import asyncio
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import *
from app.services import encoder, qdrant
from app.config import settings

from contextlib import asynccontextmanager
from .config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await encoder.initialize()
    print("Connecting to qdrant", flush=True)
    qdrant.initialize(settings.qdrant_host, settings.qdrant_port)
    
    # Only load courses if explicitly requested via environment variable
    load_courses = os.getenv("LOAD_COURSES", "false").lower() == "true"
    if load_courses:
        logger.info("LOAD_COURSES=true, starting course data loading...")
        app.state.courses_load_task = asyncio.create_task(qdrant.loadCourses())
    else:
        logger.info("LOAD_COURSES=false, skipping course data loading. Data will be loaded from existing Qdrant storage.")
    
    yield
    # Clean up the ML models and release the resources


app = FastAPI(
    docs_url="/swagger",  # вместо /docs
    redoc_url="/redocly",  # вместо /redoc
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
app.include_router(courses.router)

logger.info("Application started")


@app.get("/")
async def root():
    return {"message": "Hello Universe!"}

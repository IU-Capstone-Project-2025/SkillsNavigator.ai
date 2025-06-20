import asyncio

from fastapi import FastAPI

from .routers import *
from app.services import encoder, qdrant
from app.config import settings

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await encoder.initialize()
    print("Connecting to qdrant", flush=True)
    qdrant.initialize(settings.qdrant_host, settings.qdrant_port)
    # await qdrant.loadCourses()
    app.state.courses_load_task = asyncio.create_task(qdrant.loadCourses())
    yield
    # Clean up the ML models and release the resources


app = FastAPI(
    docs_url="/swagger",  # вместо /docs
    redoc_url="/redocly",  # вместо /redoc
    openapi_url="/api/schema",  # вместо /openapi.json
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(courses.router)


@app.get("/")
async def root():
    return {"message": "Hello Universe!"}

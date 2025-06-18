from fastapi import FastAPI

from app.routers import users
from app.services import encoder, qdrant, run_blocking
from app.config import settings

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await encoder.initialize()
    print("Connecting to qdrant")
    qdrant.initialize(settings.qdrant_host, settings.qdrant_port)
    await run_blocking(qdrant.loadCourses, "courses")
    yield
    # Clean up the ML models and release the resources
    

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello Universe!"}

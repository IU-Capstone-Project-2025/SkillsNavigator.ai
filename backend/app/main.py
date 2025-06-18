from fastapi import FastAPI

from app.routers import users
from app.services import encoder, qdrant
from app.config import settings

app = FastAPI()

app.include_router(users.router)

@app.on_event("startup")
async def startup_event():
    await encoder.initialize()
    qdrant.initialize(settings.qdrant_host, settings.qdrant_port)


@app.on_event("shutdown")
async def shutdown_event():
    pass


@app.get("/")
async def root():
    return {"message": "Hello Universe!"}

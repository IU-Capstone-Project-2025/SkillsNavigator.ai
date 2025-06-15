from fastapi import Depends, FastAPI

from .routers import users

app = FastAPI(
    docs_url="/swagger",      # вместо /docs
    redoc_url="/redocly",     # вместо /redoc
    openapi_url="/api/schema" # вместо /openapi.json
)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello Universe!"}

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from starlette.middleware.cors import CORSMiddleware

from apitally.fastapi import ApitallyMiddleware

import os
import dotenv

# Internal
from ..api.routers import shipments_router
from ..api.internal.repositories import models
from ..api.internal.repositories.database import engine
from ..utils.config import settings

dotenv.load_dotenv("../")

app = FastAPI(
    title=settings.APP_TITLE,
    summary=settings.APP_SUMMARY,
    version=settings.APP_VERSION,
    redoc_url=None,
)

# Routers
app.include_router(shipments_router.router)

# Middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
# Monitoring setup
app.add_middleware(
    ApitallyMiddleware,
    client_id=os.getenv("CLIENT_APITALLY"),
    env="prod",
)

# Models DB
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def hello_world():
    msg = {"message": "Hello World"}
    return JSONResponse(msg, status_code=200)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", port=3000, host="0.0.0.0", reload=True)

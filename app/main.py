from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.startup.load_embeddings import (
    initialize_embeddings
)

from app.api.v1.routes.health import (
    router as health_router
)

from app.api.v1.routes.chat import (
    router as chat_router
)

from app.api.v1.routes.outfit import (
    router as outfit_router
)

from app.api.v1.routes.color import (
    router as color_router
)

from app.api.v1.routes.recommendation import (
    router as recommendation_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\nStarting AskDrip...")

    initialize_embeddings()

    print("AskDrip Ready\n")

    yield

    print("Shutting Down AskDrip...")


app = FastAPI(
    title="AskDrip AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    chat_router,
    prefix="/api/v1"
)

app.include_router(
    outfit_router,
    prefix="/api/v1"
)

app.include_router(
    color_router,
    prefix="/api/v1"
)

app.include_router(
    recommendation_router,
    prefix="/api/v1"
)


@app.get("/")
def root():

    return {
        "message": "AskDrip SDK Running"
    }
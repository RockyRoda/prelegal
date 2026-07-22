from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import router as auth_router
from .db import reset_database
from .nda_chat import router as nda_chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    reset_database()
    yield


app = FastAPI(title="Prelegal API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(nda_chat_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

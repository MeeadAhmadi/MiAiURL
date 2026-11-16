from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="MiAiURL", lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}
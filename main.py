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

from pydantic import BaseModel, HttpUrl
from database import create_link


class LinkRequest(BaseModel):
    target_url: HttpUrl


@app.post("/links", status_code=201)
def shorten_link(request: LinkRequest):
    code = create_link(str(request.target_url))
    return {"code": code}

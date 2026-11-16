from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

from database import create_link, init_db, resolve_link


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="MiAiURL", lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}


class LinkRequest(BaseModel):
    target_url: HttpUrl


@app.post("/links", status_code=201)
def shorten_link(request: LinkRequest):
    code = create_link(str(request.target_url))
    return {"code": code}


@app.get("/{code}")
def redirect_link(code: str):
    target_url = resolve_link(code)
    if target_url is None:
        raise HTTPException(status_code=404, detail="Link not found")

    return RedirectResponse(url=target_url, status_code=302)
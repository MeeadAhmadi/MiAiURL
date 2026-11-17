from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl

from database import create_link, init_db, resolve_link


STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="MiAiURL", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


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
def redirect_link(code: str, request: Request):
    target_url = resolve_link(code)
    if target_url is None:
        if "text/html" in request.headers.get("accept", ""):
            return FileResponse(STATIC_DIR / "404.html", status_code=404)
        raise HTTPException(status_code=404, detail="Link not found")

    return RedirectResponse(url=target_url, status_code=302)
"""仲良しTube+ FastAPI エントリポイント。"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import api as api_router
from .routers import pages as pages_router

BASE = Path(__file__).resolve().parents[1]

app = FastAPI(title="仲良しTube+", docs_url=None, redoc_url=None)
app.add_middleware(GZipMiddleware, minimum_size=512)

static_dir = BASE / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# /api を先に登録（SPAキャッチオールより優先）
app.include_router(api_router.router)
app.include_router(pages_router.router)

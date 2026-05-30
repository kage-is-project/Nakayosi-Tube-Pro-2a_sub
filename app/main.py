"""FastAPI エントリポイント。"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import api, pages

app = FastAPI(title="仲良しTube Pro", version="1.0.0")
app.add_middleware(GZipMiddleware, minimum_size=500)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.router)
app.include_router(pages.router)  # 最後: SPA catch-all

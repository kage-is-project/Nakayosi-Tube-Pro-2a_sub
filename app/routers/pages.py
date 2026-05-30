"""元の単一HTMLをそのまま返す（SPA本体）。"""
from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse

router = APIRouter()

TEMPLATE = Path(__file__).resolve().parents[2] / "templates" / "index.html"


@router.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse(TEMPLATE, media_type="text/html; charset=utf-8")


# どの URL でも元のHTMLを返す（クライアント側でルーティング）
@router.get("/{full_path:path}", response_class=HTMLResponse)
async def spa(full_path: str):
    # /api と /static は他のルーターが先に拾うのでここには来ない
    return FileResponse(TEMPLATE, media_type="text/html; charset=utf-8")

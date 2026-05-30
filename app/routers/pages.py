"""SPA フォールバック - 全ページ用ルート (/, /home, /watch, /search, /trending, /channel/:id)。"""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SPA_PATHS = {"home", "watch", "search", "trending", "channel", "mypage"}


@router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/home", status_code=302)


@router.get("/{full_path:path}", response_class=HTMLResponse, include_in_schema=False)
async def spa(request: Request, full_path: str):
    # 旧 hash ルートを新ルートへリダイレクト (#/home → /home)
    # 注: ハッシュはサーバには届かないのでクライアント側でも処理
    return templates.TemplateResponse("index.html", {"request": request})

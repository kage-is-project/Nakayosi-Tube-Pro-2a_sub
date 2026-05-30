"""フロントエンドからの /api/inv/... を Invidious にプロキシ。"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Response

from ..proxy import race_invidious

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/health")
async def health():
    return {"ok": True, "backend": "invidious-only"}


@router.get("/inv/{path:path}")
async def inv_proxy(path: str, request: Request):
    params = dict(request.query_params)
    try:
        data, ctype = await race_invidious(path, params)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    return Response(
        content=data,
        media_type=ctype,
        headers={
            "Cache-Control": "public, max-age=30",
            "Access-Control-Allow-Origin": "*",
        },
    )

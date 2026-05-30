"""/api/* エンドポイント - 軽量クライアント向け JSON API。"""
from __future__ import annotations

from typing import Any
from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Query

from ..config import INVIDIOUS_INSTANCES, PIPED_INSTANCES
from ..proxy import race_json

router = APIRouter(prefix="/api", tags=["api"])


def _inv_urls(path: str) -> list[str]:
    return [f"{base}{path}" for base in INVIDIOUS_INSTANCES]


def _piped_urls(path: str) -> list[str]:
    return [f"{base}{path}" for base in PIPED_INSTANCES]


@router.get("/trending")
async def trending(region: str = "JP") -> Any:
    return await race_json(
        _inv_urls(f"/api/v1/trending?region={region}"),
        cache_key=f"trending:{region}",
    )


@router.get("/search")
async def search(v: str = Query(..., min_length=1, max_length=200)) -> Any:
    q = quote(v)
    return await race_json(
        _inv_urls(f"/api/v1/search?q={q}&type=video"),
        cache_key=f"search:{v}",
    )


@router.get("/video/{video_id}")
async def video(video_id: str) -> Any:
    if not video_id or len(video_id) > 32:
        raise HTTPException(400, "invalid id")
    try:
        return await race_json(
            _inv_urls(f"/api/v1/videos/{video_id}"),
            cache_key=f"video:{video_id}",
        )
    except Exception:
        return await race_json(
            _piped_urls(f"/streams/{video_id}"),
            cache_key=f"video-piped:{video_id}",
        )


@router.get("/comments/{video_id}")
async def comments(video_id: str) -> Any:
    return await race_json(
        _inv_urls(f"/api/v1/comments/{video_id}"),
        cache_key=f"comments:{video_id}",
    )


@router.get("/channel/{channel_id}")
async def channel(channel_id: str) -> Any:
    return await race_json(
        _inv_urls(f"/api/v1/channels/{channel_id}"),
        cache_key=f"channel:{channel_id}",
    )

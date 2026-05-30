"""並列フェッチユーティリティ - 複数インスタンスに同時リクエストして最速応答を採用。"""
from __future__ import annotations

import asyncio
import time
from typing import Any, Iterable

import httpx

from .config import CACHE_TTL_SEC, REQUEST_TIMEOUT

_cache: dict[str, tuple[float, Any]] = {}


def _cache_get(key: str):
    item = _cache.get(key)
    if not item:
        return None
    ts, val = item
    if time.time() - ts > CACHE_TTL_SEC:
        _cache.pop(key, None)
        return None
    return val


def _cache_set(key: str, val: Any) -> None:
    _cache[key] = (time.time(), val)


async def _fetch_one(client: httpx.AsyncClient, url: str) -> Any:
    r = await client.get(url, timeout=REQUEST_TIMEOUT, follow_redirects=True)
    r.raise_for_status()
    return r.json()


async def race_json(urls: Iterable[str], cache_key: str | None = None) -> Any:
    """与えられた URL 群に並列リクエストし、最初に成功したレスポンスを返す。"""
    if cache_key:
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

    async with httpx.AsyncClient(http2=True, headers={"User-Agent": "NakayosiTubePro/1.0"}) as client:
        tasks = [asyncio.create_task(_fetch_one(client, u)) for u in urls]
        try:
            while tasks:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for d in done:
                    tasks.remove(d)
                    try:
                        result = d.result()
                        for p in tasks:
                            p.cancel()
                        if cache_key:
                            _cache_set(cache_key, result)
                        return result
                    except Exception:
                        continue
        finally:
            for t in tasks:
                t.cancel()

    raise RuntimeError("All upstream instances failed")

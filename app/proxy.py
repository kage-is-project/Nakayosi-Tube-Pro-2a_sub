"""Invidious インスタンスを並列に叩いて最速の正常レスポンスを返す。"""
from __future__ import annotations

import asyncio
import random
import time
from typing import Any

import httpx

from .config import (
    CACHE_TTL,
    INVIDIOUS_INSTANCES,
    RACE_CONCURRENCY,
    REQUEST_TIMEOUT,
)

_cache: dict[str, tuple[float, Any, str]] = {}

_client: httpx.AsyncClient | None = None


def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT,
            follow_redirects=True,
            http2=False,
            headers={
                "User-Agent": "NakayosiTube/1.0 (+fastapi)",
                "Accept": "application/json,*/*;q=0.8",
            },
            limits=httpx.Limits(max_connections=64, max_keepalive_connections=32),
        )
    return _client


def _cache_get(key: str):
    v = _cache.get(key)
    if not v:
        return None
    ts, data, ctype = v
    if time.time() - ts > CACHE_TTL:
        _cache.pop(key, None)
        return None
    return data, ctype


def _cache_set(key: str, data: Any, ctype: str) -> None:
    _cache[key] = (time.time(), data, ctype)
    if len(_cache) > 512:
        # 古いものから削除
        for k, _ in sorted(_cache.items(), key=lambda x: x[1][0])[:128]:
            _cache.pop(k, None)


async def _one(instance: str, path: str, params: dict[str, str]) -> tuple[bytes, str]:
    url = f"{instance.rstrip('/')}/api/v1/{path.lstrip('/')}"
    client = get_client()
    r = await client.get(url, params=params)
    if r.status_code != 200:
        raise RuntimeError(f"{instance} -> {r.status_code}")
    ctype = r.headers.get("content-type", "application/json")
    return r.content, ctype


async def race_invidious(path: str, params: dict[str, str]) -> tuple[bytes, str]:
    """同一パスを複数 Invidious に並列発射し、最速の正常応答を返す。"""
    key = f"{path}?{sorted(params.items())}"
    cached = _cache_get(key)
    if cached:
        return cached

    instances = INVIDIOUS_INSTANCES.copy()
    random.shuffle(instances)

    async def runner(inst: str):
        return await _one(inst, path, params)

    # 波状に投げて最速を採用
    batch_size = RACE_CONCURRENCY
    last_err: Exception | None = None
    for i in range(0, len(instances), batch_size):
        batch = instances[i : i + batch_size]
        tasks = [asyncio.create_task(runner(x)) for x in batch]
        try:
            for fut in asyncio.as_completed(tasks):
                try:
                    data, ctype = await fut
                    # 残りをキャンセル
                    for t in tasks:
                        if not t.done():
                            t.cancel()
                    _cache_set(key, (data, ctype), ctype)
                    return data, ctype
                except Exception as e:
                    last_err = e
                    continue
        finally:
            for t in tasks:
                if not t.done():
                    t.cancel()

    raise RuntimeError(f"all invidious instances failed: {last_err}")

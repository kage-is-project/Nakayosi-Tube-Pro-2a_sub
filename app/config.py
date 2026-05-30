"""公開インスタンス一覧。並列リクエストで最速のものを採用する。"""

INVIDIOUS_INSTANCES = [
    "https://inv.nadeko.net",
    "https://invidious.nerdvpn.de",
    "https://invidious.privacyredirect.com",
    "https://yewtu.be",
    "https://invidious.f5.si",
    "https://iv.melmac.space",
    "https://yt.omada.cafe",
]

PIPED_INSTANCES = [
    "https://pipedapi.kavin.rocks",
    "https://pipedapi-libre.kavin.rocks",
    "https://pipedapi.adminforge.de",
]

REQUEST_TIMEOUT = 6.0  # 秒
CACHE_TTL_SEC = 60     # メモリキャッシュ TTL

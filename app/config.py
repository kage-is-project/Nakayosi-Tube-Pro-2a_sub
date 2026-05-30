"""Invidious のみ使用（Piped 不使用）。"""

INVIDIOUS_INSTANCES = [
    "https://inv.nadeko.net",
    "https://invidious.nerdvpn.de",
    "https://invidious.privacyredirect.com",
    "https://yewtu.be",
    "https://iv.melmac.space",
    "https://invidious.f5.si",
    "https://invidious.materialio.us",
    "https://invidious.privacydev.net",
    "https://invidious.tiekoetter.com",
    "https://invidious.protokolla.fi",
    "https://invidious.private.coffee",
    "https://invidious.lunivers.trade",
    "https://invidious.perennialte.ch",
    "https://inv.tux.pizza",
    "https://invidious.reallyaweso.me",
    "https://iv.datura.network",
    "https://invidious.adminforge.de",
    "https://invidious.einfachzocken.eu",
    "https://invidious.fdn.fr",
    "https://invidious.projectsegfau.lt",
    "https://invidious.drgns.space",
    "https://invidious.jing.rocks",
    "https://iteroni.com",
    "https://yt.cdaut.de",
]

REQUEST_TIMEOUT = 4.5  # 1 インスタンスあたりのタイムアウト
RACE_CONCURRENCY = 6   # 同時に投げる本数
CACHE_TTL = 60         # 秒

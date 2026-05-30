# 仲良しTube Pro

FastAPI + 軽量バニラJSクライアントで作る、最速・軽量な YouTube フロントエンド。
Invidious / Piped の公開インスタンスを並列フェッチして、最初に返ってきたレスポンスを採用します。

## 構成

```
nakayosi-tube-pro/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI エントリ
│   ├── config.py            # インスタンス一覧
│   ├── proxy.py             # 並列フェッチ (最速で取得)
│   └── routers/
│       ├── __init__.py
│       ├── api.py           # /api/* (検索/動画/トレンド/チャンネル)
│       └── pages.py         # SPA fallback (/home, /watch ...)
├── templates/
│   └── index.html           # SPA シェル
├── static/
│   ├── css/style.css
│   └── js/
│       ├── app.js           # ルーター + 状態管理
│       ├── api.js           # /api/* ラッパー
│       └── views/
│           ├── home.js
│           ├── search.js
│           ├── watch.js
│           ├── trending.js
│           └── channel.js
├── requirements.txt
├── render.yaml              # Render.com デプロイ設定
├── Procfile
└── runtime.txt
```

## ルーティング (pushState)

旧 `/#/home` → 新 `/home`。全てのハッシュルートを history API に置き換え。

| 旧 (hash) | 新 (pushState) |
|---|---|
| `/#/home` | `/home` |
| `/#/trending` | `/trending` |
| `/#/search?v=xxx` | `/search?v=xxx` |
| `/#/watch?v=ID` | `/watch?v=ID` |
| `/#/@CHID` | `/channel/CHID` |

## ローカル実行

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# → http://127.0.0.1:8000/home
```

## Render デプロイ

1. このリポジトリを GitHub に push
2. Render で **New +** → **Blueprint** → リポジトリを選択
3. `render.yaml` が自動検出され、Free プランでデプロイされます

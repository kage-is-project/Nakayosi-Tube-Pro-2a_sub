# 仲良しTube+ (FastAPI + Invidious)

元の単一HTMLのUIをそのまま使い、データ取得を FastAPI バックエンド経由で
Invidious 複数インスタンスへ並列リクエストする構成。**Piped は使用しません。**

## 構成

```
app/
  main.py              FastAPI アプリ
  config.py            Invidious インスタンス一覧
  proxy.py             並列レース取得 + キャッシュ
  routers/
    api.py             /api/inv/{path}  → Invidious プロキシ
    pages.py           SPA フォールバック (元HTMLを配信)
templates/
  index.html           元の 仲良しTube+ HTML (UIそのまま)
static/                予約 (使用するなら CSS/JS を追加)
```

## 仕組み

1. ブラウザ側で `fetch()` を上書きし、Invidious / CORSプロキシ宛のリクエストを
   `/api/inv/<path>` に書き換える。Piped 宛は即時失敗させる。
2. FastAPI 側で `/api/inv/<path>` を受けたら、複数 Invidious インスタンスへ
   並列リクエストし、**最速の200応答を返す**（60秒キャッシュ）。

## ローカル実行

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# → http://127.0.0.1:8000/
```

## Render デプロイ

`render.yaml` を含む Blueprint。リポジトリを Render に接続して
"New Blueprint" を選ぶだけ。

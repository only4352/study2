# WebAPI Service

FastAPIを使用したWebAPIサービスです。UbuntuベースのDockerコンテナで動作します。

## 特徴

- **FastAPI**: 高速でモダンなPython Webフレームワーク
- **ホットリロード**: 開発時のファイル変更を自動検知
- **自動APIドキュメント**: Swagger UI (/docs) と ReDoc (/redoc)
- **ヘルスチェック**: コンテナの健全性監視
- **CORS対応**: フロントエンドからのアクセスに対応

## 起動方法

### Docker Composeを使用（推奨）
```bash
# コンテナのビルドと起動
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d --build

# 停止
docker-compose down
```

### Dockerコマンドを使用
```bash
# イメージのビルド
docker build -t webapi .

# コンテナの起動
docker run -d -p 8001:8001 --name webapi webapi

# 停止
docker stop webapi
docker rm webapi
```

## アクセス

- **API**: http://localhost:8001
- **APIドキュメント**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **ヘルスチェック**: http://localhost:8001/health

## API エンドポイント

### 基本エンドポイント
- `GET /` - サービス状態確認
- `GET /health` - ヘルスチェック

### アイテム管理
- `GET /items` - 全アイテム取得
- `GET /items/{item_id}` - 特定アイテム取得
- `POST /items` - 新規アイテム作成
- `PUT /items/{item_id}` - アイテム更新
- `DELETE /items/{item_id}` - アイテム削除

## 開発

### ホットリロード
ソースコードを変更すると、自動的にサーバーが再起動されます。

### ログ確認
```bash
# コンテナのログを確認
docker-compose logs -f webapi

# または
docker logs -f webapi
```

### コンテナ内での操作
```bash
# コンテナ内に入る
docker exec -it webapi bash

# Python環境の確認
python --version
pip list
```

## ファイル構成

```
webapi/
├── Dockerfile          # コンテナ定義
├── docker-compose.yml  # サービス定義
├── main.py            # FastAPIアプリケーション
├── requirements.txt   # Python依存関係
└── README.md         # このファイル
```

## トラブルシューティング

### ポート8001が既に使用されている場合
```bash
# 使用中のポートを確認
sudo netstat -tlnp | grep :8001

# または
sudo lsof -i :8001
```

### コンテナが起動しない場合
```bash
# ログを確認
docker-compose logs webapi

# コンテナの状態確認
docker-compose ps
```

## 今後の拡張

このサービスは、将来的にDocker Composeを使用して他のサービス（データベース、キャッシュ、フロントエンドなど）と連携することを想定しています。

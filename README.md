# Container Loading Optimization App

物流コンテナの最適積載数を算出するWebアプリケーション

## 🎯 プロジェクト概要

同一商品のみを積載する物流コンテナに対し、余剰体積 ≤ 10%（目標 ≤ 5%）となる最大積載数を算出するアプリケーションです。

### 技術スタック
- **Backend**: Python 3.12 + FastAPI
- **Frontend**: React + Vite + TypeScript
- **Database**: SQLite 3
- **Deployment**: GCP Cloud Run
- **CI/CD**: Cloud Build

## 🚀 セットアップ手順

### 前提条件
- Python 3.12
- Node.js 20+
- Docker
- GCP CLI (デプロイ時)

### ローカル開発環境のセットアップ

1. **リポジトリのクローン**
```bash
git clone https://github.com/Terui-31/devin_container_optim.git
cd devin_container_optim
```

2. **環境依存パッケージのインストール**
```bash
./setup.sh
```

3. **環境変数の設定**
```bash
# direnvを使用する場合
echo 'export PYTHONPATH="."' >> .envrc
echo 'export DATABASE_URL="sqlite:///app.db"' >> .envrc
direnv allow
```

4. **バックエンドのセットアップ**
```bash
cd backend
pip install -r requirements.txt
python seed.py  # サンプルデータの投入
```

5. **フロントエンドのセットアップ**
```bash
cd frontend
npm install
```

### ローカル実行

#### 方法1: 開発モード（推奨）

**バックエンドの起動**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**フロントエンドの起動**
```bash
cd frontend
npm run dev
```

アプリケーションは http://localhost:5173 でアクセス可能です。

#### 方法2: Dockerコンテナ実行

**Dockerイメージのビルド**
```bash
docker build -t container-loading-app .
```

**コンテナの実行**
```bash
docker run -p 8080:8080 container-loading-app
```

アプリケーションは http://localhost:8080 でアクセス可能です。

### テスト実行

#### バックエンドテスト
```bash
cd backend
pytest -q
```

#### フロントエンドテスト
```bash
cd frontend
npm test
```

#### Lint実行
```bash
# Backend
cd backend
ruff check .

# Frontend
cd frontend
npm run lint
```

#### 統合テスト
```bash
# Dockerコンテナでの統合テスト
docker build -t container-loading-app .
docker run -d -p 8080:8080 --name test-container container-loading-app

# ヘルスチェック
curl http://localhost:8080/api/healthz

# API テスト
curl -X POST http://localhost:8080/api/optimize \
  -H "Content-Type: application/json" \
  -d '{"container":{"length":60,"width":40,"height":16},"sku":"SKU003"}'

# コンテナの停止と削除
docker stop test-container
docker rm test-container
```

## 🏗️ アーキテクチャ

### システム構成
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │───▶│   FastAPI       │───▶│   SQLite DB     │
│   (Frontend)    │    │   (Backend)     │    │   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### API エンドポイント
- `GET /api/healthz` - ヘルスチェック
- `GET /api/items` - 商品カタログ一覧取得
- `GET /api/items/{sku}` - 特定商品の詳細取得
- `POST /api/optimize` - 最適積載数算出

### データベーススキーマ
- `ItemCatalog` テーブル: SKU, name, length, width, height, weight

## 📋 使用方法

### 1. Webアプリケーション

1. アプリケーションにアクセス（http://localhost:5173 または http://localhost:8080）
2. コンテナ寸法を入力（長さ、幅、高さ in cm）
3. SKUドロップダウンから商品を選択
4. 「最適化実行」ボタンをクリック
5. 結果を確認：
   - 最大積載数
   - 余剰体積の割合
   - 商品詳細情報

### 2. API直接利用

**商品一覧の取得**
```bash
curl http://localhost:8000/api/items
```

**最適化計算の実行**
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "container": {
      "length": 60,
      "width": 40,
      "height": 16
    },
    "sku": "SKU003",
    "item_volume_margin": 0.95
  }'
```

**レスポンス例**
```json
{
  "max_count": 30,
  "leftover_percentage": 6.25,
  "container_volume": 38400,
  "item_volume": 1200,
  "item_details": {
    "sku": "SKU003",
    "name": "Small Box C",
    "dimensions": {
      "length": 15,
      "width": 10,
      "height": 8
    },
    "weight": 0.8
  }
}
```

### 3. サンプルデータ

アプリケーションには以下のサンプル商品が含まれています：

| SKU | 商品名 | 寸法 (L×W×H cm) | 重量 (kg) |
|-----|--------|------------------|-----------|
| SKU001 | Small Box A | 10×8×6 | 0.5 |
| SKU002 | Medium Box B | 20×15×12 | 1.2 |
| SKU003 | Small Box C | 15×10×8 | 0.8 |

## 🚀 デプロイ

### Docker デプロイ

**1. ローカルDockerでのテスト**
```bash
# イメージのビルド
docker build -t container-loading-app .

# コンテナの実行
docker run -p 8080:8080 container-loading-app

# ヘルスチェック
curl http://localhost:8080/api/healthz
```

### GCP Cloud Run デプロイ

**1. 前提条件**
```bash
# Google Cloud SDKのインストール
curl https://sdk.cloud.google.com | bash
source ~/.bashrc

# 認証とプロジェクト設定
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

**2. 手動デプロイ**
```bash
# Artifact Registryの有効化
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# リポジトリの作成
gcloud artifacts repositories create cont-load \
  --repository-format=docker \
  --location=asia-northeast1

# イメージのビルドとプッシュ
gcloud builds submit --tag asia-northeast1-docker.pkg.dev/YOUR_PROJECT_ID/cont-load/app:latest

# Cloud Runへのデプロイ
gcloud run deploy cont-load-api \
  --image asia-northeast1-docker.pkg.dev/YOUR_PROJECT_ID/cont-load/app:latest \
  --region asia-northeast1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

**3. Cloud Build経由での自動デプロイ**
```bash
# Cloud Build設定ファイルを使用
gcloud builds submit --config .cloudbuild/cloudbuild.yaml

# 環境変数の設定例
export PROJECT_ID="your-project-id"
export LOCATION="asia-northeast1"
export REGION="asia-northeast1"
```

### CI/CD

**Cloud Build トリガーの設定**
1. Google Cloud Consoleでトリガーを作成
2. リポジトリ: `Terui-31/devin_container_optim`
3. ブランチ: `^main$`
4. 設定ファイル: `.cloudbuild/cloudbuild.yaml`
5. 置換変数:
   - `_LOCATION`: `asia-northeast1`
   - `_REGION`: `asia-northeast1`

**自動デプロイフロー**
- mainブランチへのpushで自動デプロイが実行
- Cloud Buildがトリガーされ、以下の処理を実行：
  1. Dockerイメージのビルド
  2. Artifact Registryへのプッシュ
  3. Cloud Runへのデプロイ

## 📝 開発ガイドライン

### 完了の定義（Definition of Done）
1. cloudbuild.yamlトリガーによりCloud Run URLが自動発行され、UIが動作する
2. POST /optimizeの残余体積 ≤ 5%テストケースがCIでGreen
3. READMEに"Setup | Local Run | CI | Prod Run"手順が並列で記載
4. DevinがPRをself-reviewし、confidenceコメントが0.8以上

### 品質ゲート
- Lint: ruff (backend), eslint (frontend)
- Test: pytest -q
- Build: Cloud Build
- Deploy: Cloud Run プレビューURL

## 📚 ドキュメント

- [API Documentation](http://localhost:8000/docs) (ローカル実行時)
- [OpenAPI Specification](http://localhost:8000/redoc) (ローカル実行時)

### トラブルシューティング

**よくある問題と解決方法**

1. **ポートが使用中のエラー**
```bash
# プロセスの確認と終了
lsof -ti:8000 | xargs kill -9
lsof -ti:8080 | xargs kill -9
```

2. **Dockerビルドエラー**
```bash
# キャッシュをクリアしてリビルド
docker system prune -f
docker build --no-cache -t container-loading-app .
```

3. **データベース初期化エラー**
```bash
# データベースファイルの削除と再作成
rm -f backend/app.db
cd backend && python seed.py
```

4. **フロントエンドビルドエラー**
```bash
# node_modulesの再インストール
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### パフォーマンス最適化

**推奨設定**
- Cloud Run: 1 CPU, 1Gi メモリ
- 最大インスタンス数: 10
- リクエストタイムアウト: 300秒
- 同時実行数: 80

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🤝 コントリビューション

1. フィーチャーブランチを作成
2. 変更を実装
3. テストを実行
4. プルリクエストを作成

---

**Link to Devin run**: https://app.devin.ai/sessions/d1452093d7254b1fb0bf2202897af4c1
**Requested by**: Takahiro Terui (takahiroterui31@gmail.com)

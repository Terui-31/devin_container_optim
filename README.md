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

#### バックエンドの起動
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### フロントエンドの起動
```bash
cd frontend
npm run dev
```

アプリケーションは http://localhost:5173 でアクセス可能です。

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

## 🏗️ アーキテクチャ

### システム構成
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │───▶│   FastAPI       │───▶│   SQLite DB     │
│   (Frontend)    │    │   (Backend)     │    │   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### API エンドポイント
- `GET /healthz` - ヘルスチェック
- `POST /optimize` - 最適積載数算出

### データベーススキーマ
- `ItemCatalog` テーブル: SKU, name, length, width, height, weight

## 🚀 デプロイ

### Cloud Run デプロイ
```bash
# Cloud Build経由でのデプロイ
gcloud builds submit --config .cloudbuild/cloudbuild.yaml
```

### CI/CD
- mainブランチへのpushで自動デプロイが実行されます
- Cloud Buildがトリガーされ、Cloud Runにデプロイされます

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

- [Architecture README](docs/architecture.md)
- [Runbook](docs/runbook.md)
- [API Documentation](http://localhost:8000/docs) (ローカル実行時)

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

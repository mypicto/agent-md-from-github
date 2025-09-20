# GitHub PR Review Comments Collector

GitHubリポジトリのプルリクエストからレビューコメントとDiffを効率的に収集するPythonツール。
収集したデータから AI agent が参照する `AGENT.md` を生成することを目的としています。

## 🚀 概要

このツールは、指定したGitHubリポジトリのクローズされたプルリクエストから、コードレビューコメント（inline comments）と関連するDiff抜粋を自動収集します。収集したデータを構造化して保存し、後続の分析やドキュメント化を支援します。

主な機能：

- 指定期間内のクローズ済みPRのレビューコメント収集

## 📋 前提条件

### Python環境

- Python 3.8以上
- 必要なパッケージ：`pip install -r requirements.txt`

### GitHubアクセス権限

以下のいずれかのPersonal Access Tokenが必要です：

#### Fine-grained Token（推奨）

- リポジトリのコラボレーターは対象外
- 必要な権限：
  - Pull requests: Read
  - Contents: Read
  - Metadata: Read
  - Issues: Read

#### Classic Token

- 権限：`repo`（プライベートリポジトリのフルコントロール）

## 🔐 認証設定

### トークンの保存（推奨）

```bash
python scripts/src/auth.py --store-token "your_github_token_here"
```

### 一時的な使用

```bash
export GITHUB_TOKEN="your_github_token_here"
# または
python scripts/src/fetch.py --token "your_github_token_here"
```

### トークンの削除

```bash
python scripts/src/auth.py --clear-token
```

## 📖 詳細な使用方法

### 利用可能なコマンド

| コマンド | 説明 |
|----------|------|
| `fetch.py` | PRレビューコメントの収集 |
| `pop_comments.py` | 欠落サマリーの先頭PRのレビューコメントをMarkdown形式で出力 |
| `set_summary.py` | PRのレビュー要約を設定 |
| `list_summary_files.py` | 指定リポジトリのサマリーファイルを優先度でフィルタリングして一覧表示 |
| `auth.py` | GitHubトークンの管理 |

### fetch.py オプション

| オプション | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--from-date` | ✅ | 開始日（`YYYY-MM-DD`） | - |
| `--to-date` | ✅ | 終了日（`YYYY-MM-DD`） | - |
| `--timezone` | ❌ | タイムゾーン | `Asia/Tokyo` |
| `--token` | ❌ | GitHubトークン | 環境変数/キーリング |
| `--verbose` | ❌ | 詳細出力 | `False` |

- リポジトリ情報は `workspace/workspace.yml` から取得します。

### pop_comments.py オプション

- リポジトリ情報は `workspace/workspace.yml` から取得します。

### set_summary.py オプション

| オプション | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--repo` | ✅ | リポジトリ名（`owner/repo`形式） | - |
| `--pr` | ✅ | PR番号 | - |
| `--priority` | ✅ | 優先度（`high`, `middle`, `low`） | - |
| `--file` | ✅ | 要約ファイルのパス（Markdown形式） | - |

### list_summary_files.py オプション

| オプション | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--repo` | ✅ | リポジトリ名（`owner/repo`形式） | - |
| `--priority` | ❌ | 優先度でフィルタリング（`high`, `middle`, `low`、複数指定可） | 全て |

### auth.py オプション

| オプション | 説明 |
|-----------|------|
| `--store-token` | トークンをキーリングに保存 |
| `--clear-token` | 保存トークンを削除 |

## 📁 出力形式

### ディレクトリ構造

```text
workspace/
├── workspace.yml  # リポジトリ設定ファイル
└── pullrequests/
    ├── 2025-09-01/
    │   ├── PR-123.json
    ├── 2025-09-02/
    │   ├── PR-456.json
    └── summaries/
        ├── PR-123.yml
        └── PR-456.yml
```

## ⚠️ トラブルシューティング

### よくあるエラー

| エラーコード | 原因 | 対処法 |
|-------------|------|--------|
| 401 | 認証失敗 | トークンの権限を確認 |
| 403 | レート制限超過 | 時間を置いて再試行 |
| 404 | リポジトリアクセス不可 | リポジトリ名と権限を確認 |

### 追加のヒント

- タイムゾーン設定で日付フィルタリングを調整


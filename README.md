# GitHub PR Review Comments Collector

GitHubリポジトリのプルリクエストからレビューコメントとDiffを効率的に収集するPythonツール。
収集したデータから AI agent が参照する `AGENT.md` を生成することを目的としています。

## 🚀 概要

このツールは、指定したGitHubリポジトリのクローズされたプルリクエストから、コードレビューコメント（inline comments）と関連するDiff抜粋を自動収集します。収集したデータを構造化して保存し、後続の分析やドキュメント化を支援します。

主な機能：

- 指定期間内のクローズ済みPRのレビューコメント収集
- 収集データの管理ユーティリティ

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

## 🛠️ クイックスタート

### 基本的な収集

```bash
python scripts/src/fetch.py --repo "owner/repository" --from-date "2025-09-01" --to-date "2025-09-10"
```

### サマリーデータ欠如チェック

```bash
python scripts/src/list_missing_summaries.py --repo "owner/repository"
```

### PRコメントの出力

```bash
python scripts/src/get_comments.py --repo "owner/repository" --pr PR-123
```

## 📖 詳細な使用方法

### 利用可能なコマンド

| コマンド | 説明 |
|----------|------|
| `fetch.py` | PRレビューコメントの収集 |
| `list_missing_summaries.py` | サマリーが作成されていないレビューコメントの検索 |
| `delete_summaries.py` | サマリーデータの削除 |
| `get_comments.py` | 指定PRのレビューコメントをMarkdown形式で出力 |
| `set_summary.py` | PRのレビュー要約を設定 |
| `auth.py` | GitHubトークンの管理 |

### fetch.py オプション

| オプション | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--repo` | ✅ | リポジトリ名（`owner/repo`形式） | - |
| `--from-date` | ✅ | 開始日（`YYYY-MM-DD`） | - |
| `--to-date` | ✅ | 終了日（`YYYY-MM-DD`） | - |
| `--output-dir` | ❌ | 出力ディレクトリ | `pullrequests` |
| `--timezone` | ❌ | タイムゾーン | `Asia/Tokyo` |
| `--token` | ❌ | GitHubトークン | 環境変数/キーリング |
| `--verbose` | ❌ | 詳細出力 | `False` |

### list_missing_summaries.py オプション

| オプション | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--repo` | ✅ | リポジトリ名（`owner/repo`形式） | - |
| `--output-dir` | ❌ | 出力ディレクトリ | `pullrequests` |

### delete_summaries.py オプション

| オプション | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--repo` | ❌ | リポジトリ名（`owner/repo`形式、全リポジトリ対象時は未指定） | - |
| `--output-dir` | ❌ | 出力ディレクトリ | `pullrequests` |

### get_comments.py オプション

| オプション | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--repo` | ✅ | リポジトリ名（`owner/repo`形式） | - |
| `--pr` | ✅ | PR番号（`PR-<number>`形式） | - |
| `--output-dir` | ❌ | 出力ディレクトリ | `pullrequests` |

### set_summary.py オプション

| オプション | 必須 | 説明 | デフォルト |
|-----------|------|------|-----------|
| `--repo` | ✅ | リポジトリ名（`owner/repo`形式） | - |
| `--pr` | ✅ | PR番号 | - |
| `--priority` | ✅ | 優先度（`high`, `middle`, `low`） | - |
| `--summary` | ✅ | 要約テキスト（複数行対応） | - |

### auth.py オプション

| オプション | 説明 |
|-----------|------|
| `--store-token` | トークンをキーリングに保存 |
| `--clear-token` | 保存トークンを削除 |

## 📁 出力形式

### ディレクトリ構造

```text
pullrequests/
├── owner/
│   └── repository/
│       ├── 2025-09-01/
│       │   ├── PR-123-metadata.json
│       │   └── PR-123-summary.md
│       └── 2025-09-02/
│           ├── PR-456-metadata.json
│           └── PR-456-summary.md
```

### JSONデータ形式

各PRのコメントデータは以下の構造で保存されます：

```json
{
  "pr_number": 123,
  "closed_at_iso": "2025-09-01T12:34:56+09:00",
  "merged": true,
  "review_comments": [
    {
      "id": 4567890,
      "path": "src/app.py",
      "original_position": 42,
      "commit_id": "abc123def456...",
      "user": "reviewer1",
      "created_at": "2025-08-31T10:00:00+09:00",
      "body": "ここは例外処理を追加したいです",
      "context_patch_excerpt": "@@ -40,6 +40,9 @@\n def process_data(data):\n+    if not data:\n+        raise ValueError('Data is required')\n     return data.upper()\n"
    }
  ]
}
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


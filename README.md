# GitHub PR Review Comments Collector

GitHubリポジトリの指定期間内にクローズされたプルリクエストから、**コードレビューコメント**（inline review comments）と**関連するDiff抜粋**を収集するPythonスクリプトです。

## 特徴

- ✅ **期間指定**: 指定した日付範囲でクローズされたPRを対象
- ✅ **タイムゾーン対応**: Asia/Tokyo基準での日付判定
- ✅ **レビューコメント特化**: インラインレビューコメントのみを収集（通常のコメントは除外）
- ✅ **冪等性**: 既存ファイルがある場合はスキップ
- ✅ **効率的なAPI利用**: 基本情報取得と詳細取得を分離し、不要なAPI呼び出しを削減
- ✅ **適切な権限管理**: Fine-grained personal access tokenに対応
- ✅ **構造化出力**: JSON + Patchファイル形式

## 処理フロー

1. **基本情報取得**: PRの番号、タイトル、クローズ日時、マージ状態を取得
2. **ファイル存在チェック**: 既にダウンロード済みのファイルがある場合はスキップ
3. **詳細取得**: レビューコメントとDiff情報を取得
4. **ファイル出力**: 収集したデータを構造化して保存

この設計により、APIレート制限を効率的に回避し、処理時間を短縮しています。

## 必要な権限

GitHub Fine-grained personal access tokenで以下の権限が必要です：

- **Pull requests**: Read
- **Contents**: Read  
- **Metadata**: Read
- **Issues**: Read

## インストール

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. GitHubトークンの設定

```bash
# 環境変数として設定（推奨）
export GITHUB_TOKEN="your_github_token_here"

# または実行時に--tokenオプションで指定
```

## 使用方法

### 基本的な使用例

```bash
# 環境変数でトークンを設定している場合
python prcollector/src/main.py --repo "octo-org/example" --from-date "2025-09-01" --to-date "2025-09-10"

# トークンを直接指定する場合
python prcollector/src/main.py --repo "octo-org/example" --from-date "2025-09-01" --to-date "2025-09-10" --token "your_token"
```

### 高度な使用例

```bash
# 出力ディレクトリとタイムゾーンを指定
python prcollector/src/main.py \
  --repo "owner/repository" \
  --from-date "2025-08-01" \
  --to-date "2025-08-31" \
  --output-dir "my_output" \
  --timezone "UTC" \
  --verbose
```

### コマンドラインオプション

| オプション | 必須 | 説明 | デフォルト値 |
|-----------|------|------|-------------|
| `--repo` | ✅ | リポジトリ名（`owner/repo`形式） | - |
| `--from-date` | ✅ | 開始日（`YYYY-MM-DD`形式、含む） | - |
| `--to-date` | ✅ | 終了日（`YYYY-MM-DD`形式、含む） | - |
| `--output-dir` | ❌ | 出力ディレクトリ | `pullrequests` |
| `--timezone` | ❌ | タイムゾーン | `Asia/Tokyo` |
| `--token` | ❌ | GitHubトークン | 環境変数`GITHUB_TOKEN` |
| `--verbose` | ❌ | 詳細ログ出力 | False |

## 出力仕様

### ディレクトリ構造

```text
pullrequests/
├── 2025-09-01/
│   ├── PR-123-comments.json
│   ├── PR-123-diff.patch
│   ├── PR-124-comments.json
│   └── PR-124-diff.patch
├── 2025-09-02/
│   ├── PR-125-comments.json
│   └── PR-125-diff.patch
└── ...
```

### JSON出力形式（`PR-{number}-comments.json`）

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

### Diff出力形式（`PR-{number}-diff.patch`）

```markdown
# PR #123: Fix data validation
# Closed at: 2025-09-01 12:34:56+00:00
# Merged: True

## File: src/app.py

### Comment by reviewer1 at position 42
Comment: ここは例外処理を追加したいです

```diff
@@ -40,6 +40,9 @@
 def process_data(data):
+    if not data:
+        raise ValueError('Data is required')
     return data.upper()
```

## 技術仕様

### 対象となるPR

- **クローズ済み**: `state='closed'`のPR
- **マージ・非マージ両方**: `merged=true`と`merged=false`の両方
- **期間内**: `closed_at`が指定期間内（タイムゾーン考慮）

### 対象となるコメント

- **レビューコメントのみ**: `PullRequest.get_review_comments()`で取得
- **インラインコメント**: コードの特定行に対するコメント
- **除外**: 通常のPRコメント（`PullRequest.get_issue_comments()`）

### 冪等性の実装

- `PR-{number}-comments.json`ファイルの存在をチェック
- 既存ファイルがある場合はPR全体をスキップ
- 部分的な実行の再開が可能

## エラーハンドリング

### よくあるエラーと対処法

#### 1. 認証エラー

```text
Error: Failed to access repository owner/repo: 401 {...}
```

**対処法**: GitHubトークンの権限を確認し、必要な権限が付与されているか確認してください。

#### 2. レート制限エラー

```text
Error: 403 API rate limit exceeded
```

**対処法**: GitHub APIのレート制限に達しています。しばらく待ってから再実行してください。

#### 3. リポジトリアクセスエラー

```text
Error: Failed to access repository owner/repo: 404 {...}
```

**対処法**: リポジトリ名が正しいか、トークンにそのリポジトリへのアクセス権限があるか確認してください。

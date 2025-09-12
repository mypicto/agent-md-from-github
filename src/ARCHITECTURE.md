# Clean Architecture - Design Documentation

## 🏗️ アーキテクチャ概要

この再設計では、Robert C. Martin の Clean Architecture 原則に従って、元のモノリシックな `PRCollector` クラスを目的駆動の複数のコンポーネントに分割しました。

## 📋 設計原則の適用

### 1. Single Responsibility Principle (SRP)

**Before**: `PRCollector` が複数の責任を持っていた
- GitHub API接続
- データ変換
- ファイル出力
- ロギング設定
- 日時変換

**After**: 各クラスが単一の責任を持つ
- `GitHubRepository`: GitHub API操作のみ
- `TimezoneConverter`: タイムゾーン変換のみ  
- `JsonOutputFormatter`: JSON形式の出力のみ
- `FileSystemOutputWriter`: ファイルシステムへの書き込みのみ
- `PRReviewCollectionService`: アプリケーションロジックの調整のみ

### 2. Open/Closed Principle (OCP)

**Before**: 新しい出力形式やフィルタリング条件の追加で既存コードの修正が必要

**After**: インターフェースを使用して拡張可能
```python
# 新しい出力形式を追加する場合
class XmlOutputFormatter:
    def format_comments(self, pr_metadata: PullRequestMetadata) -> str:
        # XML形式の実装
        pass

# 新しい出力先を追加する場合  
class S3OutputWriter:
    def write_pr_data(self, pr_metadata, comments_content, diff_content, output_directory):
        # S3への書き込み実装
        pass
```

### 3. DRY (Don't Repeat Yourself)

**Before**: 日時変換やエラーハンドリングが重複

**After**: 共通機能を専用クラスに集約
- `TimezoneConverter`: 日時変換ロジックの一元化
- `GitHubApiError`: GitHub API エラーの統一処理

### 4. Law of Demeter (LoD)

**Before**: PRオブジェクトの内部構造に深く依存
```python
# 悪い例
comment.user.login  # PR -> comment -> user -> login
```

**After**: 適切な抽象化レイヤーで依存関係を制限
```python
# 良い例
review_comment = ReviewComment(author=comment.user.login, ...)
```

### 5. KISS (Keep It Simple, Stupid)

**Before**: 1つの巨大なクラスで複雑

**After**: 小さく理解しやすいクラスに分割

## 🏛️ レイヤー構造

```
┌─────────────────────────────────────┐
│            Presentation             │  
│         (CLI Interface)             │
├─────────────────────────────────────┤
│          Application Layer          │
│    (PRReviewCollectionService)      │  
├─────────────────────────────────────┤
│           Domain Layer              │
│   (Models, Value Objects, Rules)    │
├─────────────────────────────────────┤  
│        Infrastructure Layer         │
│  (GitHub API, File System, etc.)    │
└─────────────────────────────────────┘
```

### Presentation Layer (`cli.py`)
- ユーザーからの入力を受け取る
- コマンドライン引数の解析
- エラーメッセージの表示

### Application Layer (`application_service.py`)
- ビジネスロジックの調整
- トランザクション境界の管理
- 複数のドメインサービスの組み合わせ

### Domain Layer (`models.py`)
- ビジネスルールとロジック
- Value Objects (不変オブジェクト)
- ドメインサービス

### Infrastructure Layer
- `github_repository.py`: GitHub API との通信
- `output_services.py`: ファイルシステムへの出力
- `timezone_converter.py`: 外部ライブラリ (pytz) のラッピング

## 🎯 主要な改善点

### 1. テスタビリティの向上
各コンポーネントが独立してテスト可能:
```python
# モックを使用したテストが容易
def test_timezone_converter():
    converter = TimezoneConverter("UTC")
    result = converter.convert_to_target_timezone(utc_datetime)
    assert result.tzinfo.zone == "UTC"
```

### 2. 拡張性の向上
新機能の追加が既存コードに影響しない:
```python
# 新しい出力形式を追加
class MarkdownOutputFormatter(OutputFormatterInterface):
    def format_comments(self, pr_metadata: PullRequestMetadata) -> str:
        # Markdown実装
        pass
```

### 3. 可読性の向上
- 各クラスの目的が明確
- インターフェースで依存関係が明示的
- ドメインモデルでビジネス概念が表現

### 4. メンテナンス性の向上
- 変更の影響範囲が限定的
- 責任が分離されているため、バグの特定が容易
- コードの再利用が可能

## 📚 使用パターン

### Strategy Pattern
出力形式の選択:
```python
# JSON形式
formatter = JsonOutputFormatter()

# 将来的に XML形式を追加
formatter = XmlOutputFormatter()
```

### Factory Pattern  
依存関係の組み立て:
```python
service = ServiceFactory.create_pr_collection_service(
    github_token=token,
    timezone="Asia/Tokyo"
)
```

### Repository Pattern
データアクセスの抽象化:
```python
# GitHub APIの詳細を隠蔽
github_repo = GitHubRepository(github_client, timezone_converter)
prs = github_repo.find_closed_pull_requests_in_range(repo_id, date_range)
```

## 🔄 実行フロー

1. **CLI**: ユーザー入力を受け取り、バリデーション
2. **Factory**: 必要なサービスを組み立て
3. **Application Service**: ビジネスロジックを調整
4. **GitHub Repository**: PRデータを取得
5. **Timezone Converter**: 日時をターゲットタイムゾーンに変換
6. **Output Formatter**: データを指定形式にフォーマット
7. **Output Writer**: ファイルシステムに出力

## 🧪 拡張例

### 新しい出力形式の追加
```python
class CsvOutputFormatter(OutputFormatterInterface):
    def format_comments(self, pr_metadata: PullRequestMetadata) -> str:
        # CSV形式の実装
        pass
```

### 新しいデータソースの追加
```python
class GitLabRepository(GitHubRepositoryInterface):
    def find_closed_pull_requests_in_range(self, repo_id, date_range):
        # GitLab API の実装
        pass
```

### フィルタリング条件の追加
```python
@dataclass(frozen=True)
class AuthorFilter:
    allowed_authors: List[str]
    
    def matches(self, comment: ReviewComment) -> bool:
        return comment.author in self.allowed_authors
```

この設計により、元のコードの機能を保持しながら、保守性、拡張性、テスタビリティを大幅に向上させました。
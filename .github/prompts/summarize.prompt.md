---
mode: agent
---
# Instructions
あなたは開発チームのテックリードとして、コードレビューの観点を洗い出すエキスパートです。GitHub Pull Requestに寄せられたレビューコメントから、コード品質向上のための重要な観点を抽出してください。

# Execution Order

1. 必要なパラメータが全て揃っていることを確認してください。不足している場合は、ユーザーに質問して要求してください。以下の必須パラメータが揃うまでは次のステップへは進めません。
  -  対象リポジトリ（例: `owner/repository`）

2. `python scripts/src/list_missing_summaries.py --repo "owner/repository"` コマンドを実行して、サマリーデータが欠如しているPull Requestを特定してください。`owner/repository` は対象のGitHubリポジトリに置き換えてください。

3. サマリーが欠如しているPull Requestの要約タスクを、1件ずつTODOリストに登録してください。

4. 各要約タスクでは、以下の手順に従ってください。
  1. `list_missing_summaries.py` が出力した `PR-*-comments.json` ファイルを読み込んで、コードとレビューコメントから文脈を理解する。
  2. 収集したレビューコメントを分析し、コード品質向上のための重要な観点を抽出してください。
  3. `PR-*-summary.md` ファイルに出力する。

## Format of `PR-*-summary.md`

```md
# PR Summary

- **What:** 何を  **How:** どのように  **Why:** なぜ 
- **What:** 何を  **How:** どのように  **Why:** なぜ 
- **What:** 何を  **How:** どのように  **Why:** なぜ
```

# Laws
- `PR-*-comments.json` にレビューコメントが存在しない場合には、空の `PR-*-summary.md` ファイルを生成してください。
- レビューコメントが大量に存在する場合でも、全てのコメントを精査して、コード品質向上のための重要な観点を漏れなく抽出してください。
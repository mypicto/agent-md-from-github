---
mode: agent
---
あなたはテックリード兼プロンプトエンジニアである。
目的：レビュー要約（`list_summary_files.py` で確認）から重要な観点を抽出し、`templates/agent-template.md`に準拠したコーディング方針をデータベース化してから、ワークスペース直下に最終成果物としての `AGENT.md` を更新する。

# Execution Order

1. **必須パラメータの確認**
   * 対象リポジトリ（形式：`owner/repository`）。不足していればユーザーに確認して取得する。

2. **テンプレートの読込**
   * `templates/agent-template.md`を開き、構造（見出し構成）とスタイル（文体・表現）を把握する。

3. **要約ファイル一覧の取得**
   * 次のコマンドを実行し、優先度 High のPR要約ファイルパスを収集する（`./temp`が無ければ作成しておく）。

   ```bash
   python scripts/src/list_summary_files.py --repo "<owner/repository>" --priority high > ./temp/list_summary_files_output.md
   ```

4. **レビュー精読とルール抽出**
   * `temp/list_summary_files_output.md`に記載されたすべてのファイルを読み込む。
   * レビューコメントを精査し、コーディング規約・設計・品質に関わる重要観点を抽出する。
   * `memorys/coding-instructions-knowledge-base.md`を更新する（追記・統合・不要箇所の削除を含む）。

5. **整理と矛盾解消**
   * 重複・言い換えを統合する。
   * 矛盾は「**重大性 > 再現性 > 影響範囲**」の優先で解決する。

6. **テンプレート統合と最終成果物の生成**
   * 抽出した観点をテンプレート各セクションにマッピングし、不足セクションは合理的に追加する。
   * 既存の`./AGENT.md`があれば読み込み、重複を整理しつつ新しい観点を統合する。
   * 文章はすべて**肯定的な命令形**に統一し、`/AGENT.md`としてワークスペース直下に保存する。

# Laws

* 開発チームにとって有用と推定できる観点は採用する。少数意見でも重大性が高い場合は採用する。
* `AGENT.md`には前置きやメタ情報を一切**含めない**。

## Helps

### list_summary_files.py

```bash
usage: list_summary_files [-h] --repo REPO [--priority {high,middle,low}]
List summary files by priority

options:
  -h, --help                   show this help message and exit
  --repo REPO                  Repository in 'owner/repo' format
  --priority {high,middle,low} Priority level to filter by (can be specified multiple times)
```

# ライセンスチェッカー

商用利用制限のあるコードを検出し、Gitコミットを制御するツールです。

## 機能

- ✅ **商用利用可能なライセンス**: MIT, Apache 2.0, BSD-3-Clause, ISC, Unlicense
- ❌ **禁止されるライセンス**: GPL, AGPL, LGPL, MPL-2.0, CC-BY-SA
- 🔍 **自動チェック**: Git pre-commitフックで自動実行
- 📋 **ステージングファイル**: コミット対象ファイルのみチェック
- 🚫 **コミットブロック**: 問題のあるファイルはコミット不可

## 使用方法

### 1. 手動チェック

```bash
# ワークスペース全体をチェック
python3 scripts/license_checker.py

# ステージングされたファイルのみチェック
python3 scripts/license_checker.py --staged-only

# 特定のワークスペースをチェック
python3 scripts/license_checker.py --workspace /path/to/workspace
```

### 2. Git pre-commitフック

pre-commitフックが自動的に設定されています。コミット時に自動でライセンスチェックが実行されます。

### 3. テスト

```bash
# ライセンスチェッカーのテスト
python3 scripts/test_license_checker.py
```

## 設定

### 除外ファイル・ディレクトリ

以下のファイル・ディレクトリは自動的に除外されます：

- `.git/`, `node_modules/`, `__pycache__/`
- `build/`, `dist/`, `.cache/`, `coverage/`
- `*.pyc`, `*.log`, `*.tmp`, `*.swp`

### カスタマイズ

`scripts/license_checker.py`の以下の定数を編集してカスタマイズできます：

- `ALLOWED_LICENSES`: 許可されるライセンス
- `BLOCKED_LICENSES`: 禁止されるライセンス
- `EXCLUDED_PATTERNS`: 除外するファイル・ディレクトリ

## トラブルシューティング

### コミットがブロックされる場合

1. エラーメッセージを確認
2. 問題のあるファイルを修正
3. 再度コミットを試行

### フックが動作しない場合

```bash
# フックの実行権限を確認
ls -la .git/hooks/pre-commit

# 必要に応じて権限を設定
chmod +x .git/hooks/pre-commit
```

## ライセンス

MIT License

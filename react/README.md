# React アプリケーション

このプロジェクトは、Viteを使用して作成されたReactアプリケーションのテンプレートです。

## 機能

- ⚡️ Viteによる高速な開発環境
- ⚛️ React 18.2
- 🎨 モダンなUIデザイン
- 📱 レスポンシブデザイン
- 🔧 ESLintによるコード品質管理

## セットアップ

### 依存関係のインストール

```bash
npm install
```

### 開発サーバーの起動

```bash
npm run dev
```

開発サーバーが起動したら、ブラウザで `http://localhost:5173` を開いてください。

### ビルド

```bash
npm run build
```

### プレビュー

```bash
npm run preview
```

## プロジェクト構造

```
react-app/
├── public/          # 静的ファイル
├── src/             # ソースコード
│   ├── App.jsx      # メインコンポーネント
│   ├── App.css      # アプリケーションスタイル
│   ├── main.jsx     # エントリーポイント
│   └── index.css    # グローバルスタイル
├── index.html       # HTMLテンプレート
├── package.json     # 依存関係とスクリプト
├── vite.config.js   # Vite設定
└── .eslintrc.cjs    # ESLint設定
```

## カスタマイズ

- `src/App.jsx` を編集してアプリケーションの機能を変更
- `src/App.css` でスタイルをカスタマイズ
- `src/index.css` でグローバルスタイルを調整

## 学習リソース

- [React公式ドキュメント](https://react.dev)
- [Vite公式ドキュメント](https://vitejs.dev)
- [React Hooks](https://react.dev/reference/react/hooks)

## ライセンス

MIT

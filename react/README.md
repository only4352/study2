# React 18 + Vite プロジェクト

このプロジェクトは、Vite を使用した React 18 アプリケーションです。

## 特徴

- 🚀 **React 18**: 最新の React 機能を使用
- ⚡ **Vite**: 超高速な開発サーバーとビルドツール
- 💻 **モダン**: ES6+モジュールと JSX
- 📱 **レスポンシブ**: モバイルとデスクトップの両方に対応

## 使用方法

### 1. 依存関係のインストール

```bash
npm install
```

### 2. 開発サーバーの起動

```bash
npm run dev
```

### 3. ビルド

```bash
npm run build
```

### 4. プレビュー

```bash
npm run preview
```

## ファイル構成

```
react/
├── index.html              # メインのHTMLファイル
├── vite.config.js          # Vite設定
├── src/
│   ├── main.jsx            # React 18エントリーポイント
│   ├── App.jsx             # メインコンポーネント
│   ├── App.css             # コンポーネントスタイル
│   └── index.css           # ベーススタイル
├── package.json            # 依存関係とスクリプト
└── README.md               # このファイル
```

## 技術仕様

- **React**: 18.2.0
- **Vite**: 4.5.0
- **@vitejs/plugin-react**: 4.2.0
- **Node.js**: 18.14.0 以上

## 開発サーバーについて

Vite は開発時に以下の利点を提供します：

- ⚡ **超高速起動**: 数秒で開発サーバーが起動
- 🔄 **HMR**: ファイル変更時の即座な更新
- 📦 **ES6 モジュール**: ネイティブ ES6 モジュールを使用
- 🎯 **最適化**: 開発時は必要な部分のみ処理

## カスタマイズ

### コンポーネントの追加

```bash
# 新しいコンポーネントを作成
touch src/NewComponent.jsx
```

### スタイルの変更

```css
/* src/App.css でスタイルを編集 */
.App {
  /* カスタムスタイル */
}
```

## トラブルシューティング

### 開発サーバーが起動しない

```bash
# 依存関係を再インストール
rm -rf node_modules
npm install
```

### ビルドエラー

```bash
# Viteのキャッシュをクリア
npm run build -- --force
```

## ライセンス

MIT License - 商用利用可能

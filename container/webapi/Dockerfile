# Ubuntu 22.04 LTSをベースイメージとして使用
FROM ubuntu:22.04

# 環境変数の設定
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# システムパッケージの更新とPython関連パッケージのインストール
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python3をpythonとして使用できるようにシンボリックリンクを作成
RUN ln -s /usr/bin/python3 /usr/bin/python

# 作業ディレクトリの設定
WORKDIR /app

# Python仮想環境の作成
RUN python3 -m venv /opt/venv

# 仮想環境をアクティベートするためのパス設定
ENV PATH="/opt/venv/bin:$PATH"

# pipのアップグレード
RUN pip install --upgrade pip

# requirements.txtをコピーして依存関係をインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリケーションコードをコピー
COPY main.py .

# ポート8001を公開
EXPOSE 8001

# ヘルスチェックの設定
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# コンテナ起動時のコマンド
CMD ["python", "main.py"]

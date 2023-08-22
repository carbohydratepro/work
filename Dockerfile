# ベースとなるイメージを指定
FROM python:3.9

# 環境変数を設定 (Pythonが.pycファイルを生成しないように)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを設定
RUN mkdir /code
WORKDIR /code

# 依存関係をインストール
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# プロジェクトのファイルをコンテナにコピー
COPY . /work/

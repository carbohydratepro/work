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

# メモリを解放するためにキャッシュを削除
RUN rm -rf /root/.cache/pip/

# gunicorn環境セッティング
RUN mkdir -p /var/run/gunicorn
CMD ["gunicorn", "project.wsgi:application", "--bind=unix:/var/run/gunicorn/gunicorn.sock"]

# プロジェクトのファイルをコンテナにコピー
COPY . /code/

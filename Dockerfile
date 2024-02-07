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

# Tesseract-OCRのインストール
RUN apt-get update && apt-get install -y tesseract-ocr-jpn


# Tesseractの最適化された日本語データのダウンロードとインストール
RUN apt-get install -y wget && \
    wget https://github.com/tesseract-ocr/tessdata_best/blob/master/jpn.traineddata -P /usr/share/tesseract-ocr/4.00/tessdata/ && \
    wget https://github.com/tesseract-ocr/tessdata_best/blob/master/jpn_vert.traineddata -P /usr/share/tesseract-ocr/4.00/tessdata/

# libGL のインストール
RUN apt-get install -y libgl1-mesa-glx

# メモリを解放するためにキャッシュを削除
RUN rm -rf /root/.cache/pip/

# gunicorn環境セッティング
RUN mkdir -p /var/run/gunicorn
CMD ["gunicorn", "project.wsgi:application", "--bind=unix:/var/run/gunicorn/gunicorn.sock", "--timeout", "120"]


# プロジェクトのファイルをコンテナにコピー
COPY . /code/

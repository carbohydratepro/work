# ワークスケジュール管理サイト

### 開発
Djangoアプリケーション作成コマンド
```text
django-admin startproject myproject
```
### 0. 立ち上げ
```text
git clone https://github.com/carbohydratepro/work
cd work
docker-compose up --build
```
アクセスできるか確認
```text
localhost:8000/calendar
```
頻繁に使用するコマンド一覧
```text
docker-comopse up -d
docker-compose down
docker-compose exec web python --version
```

### 999. コマンド
データベースの構成を完全削除してから作り直す方法
```text
docker-compose exec db psql -U myuser -d postgres
DROP DATABASE mydatabase;　
CREATE DATABASE mydatabase;
\q
docker-compose exec web python manage.py migrate
```

データベースのデータのみ削除してから作り直す方法
```text
docker-compose exec db psql -U myuser -d postgres
DELETE DATABASE mydatabase;　
\q
```

セッション削除
```text
SELECT pid, usename, application_name, client_addr, state FROM pg_stat_activity WHERE datname = 'mydatabase';
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'mydatabase';
```

管理者ユーザーの作成
```text
docker-compose exec web python manage.py createsuperuser
```

### 使用技術
   | 要素 | 名称 | バージョン |
   |---|---|---|
   | フレームワーク | Django |  |
   | 言語 | Python | 3.9 |
   | 言語 | JavaScript |  |
   | 言語 | HTML&CSS |  |
   | データベース | PostgeSQL |  |
   | クラウド/インフラ | DockerDesktop |  |
   | クラウド/インフラ | AWS or GCP |  |
   | ライブラリ | 気が向いたら記述 |  |
   
### 参考
###### plotly
```text
https://qiita.com/studio_haneya/items/b689b4c27acbd12a888d
```

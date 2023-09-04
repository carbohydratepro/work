# ワークスケジュール管理サイト

### 開発
```text
Djangoアプリケーション作成コマンド
django-admin startproject myproject

```
### 0 立ち上げ
```text
docker-compose up --build
```

### 999 コマンド
データベース完全削除
docker-compose exec db psql -U myuser -d postgres
DROP DATABASE mydatabase;　
CREATE DATABASE mydatabase;
\q
docker-compose exec web python manage.py migrate

データベース削除
docker-compose exec db psql -U myuser -d postgres
DELETE DATABASE mydatabase;　
\q

セッション削除
SELECT pid, usename, application_name, client_addr, state FROM pg_stat_activity WHERE datname = 'mydatabase';
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'mydatabase';

管理者
docker-compose exec web python manage.py createsuperuser
### 参考
plotly
https://qiita.com/studio_haneya/items/b689b4c27acbd12a888d
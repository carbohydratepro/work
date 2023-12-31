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

### 1. 開発環境時コマンド
```text
docker-compose -f docker-compose-dev.yml [down, build, up, exec...]
```

### 2. 本番環境時コマンド
```text
docker-compose build
docker-compose up -d
docker-compose exec gunicorn python manage.py makemigrations
docker-compose exec gunicorn python manage.py migrate
docker-compose exec gunicorn python manage.py collectstatic
```

### 101. メンテナンスモード及び実行
```text
docker-compose exec gunicorn python manage.py maintenance_mode on
docker-compose down
git status # ブランチ確認
git pull origin main
docker-compose up -d --build
docker-compose exec gunicorn python manage.py makemigrations
docker-compose exec gunicorn python manage.py migrate
docker-compose exec gunicorn python manage.py maintenance_mode off
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

データベースの状態確認
```text
docker-compose exec web python manage.py showmigrations
```
※auth_appの0001_initialが[ ]だった場合
```text
project/setting.py
INSTALLED_APPS = [
    'django.contrib.admin' # この行をコメントアウト
   :
]
project/urls.py
urlpatterns = [
    path('admin/', admin.site.urls), # この行をコメントアウト
   :
]

1. docker-compose exec web python manage.py migrate
2. コメントアウトをはずす
3. docker-compose exec web python manage.py migrate
エラーが生じなければ成功
```

seacret_key再生成
```text
docker-compose exec web python manage.py shell

from django.core.management.utils import get_random_secret_key
secret_key = get_random_secret_key()
text = 'SECRET_KEY = \'{0}\''.format(secret_key)
print(text)
```

### 1000. デプロイ
```text
staticファイルをappと同階層に配置。
以下のファイルにて、staticファイル関係のパスを設定。
- project/settings.py
- docker-compose.yml
- gunicorn.conf

以下のコマンドでstaticファイルを一つにまとめる。
docker-compose exec gunicorn python manage.py collectstatic
```

### 使用技術
   | 要素 | 名称 | バージョン |
   |---|---|---|
   | フレームワーク | Django | 3.2 |
   | 言語 | Python | 3.9 |
   | ライブラリ | psycog2 | 2.8 |
   | ライブラリ | plotly |  |
   | 言語 | JavaScript |  |
   | 言語 | HTML&CSS |  |
   | ライブラリ | Bootstrap |  |
   | データベース | PostgeSQL | 13 |
   | クラウド/インフラ | DockerDesktop |  |
   | クラウド/インフラ | AWS |  |
   | クラウド/インフラ | AWS/EC2 |  |
   | クラウド/インフラ | AWS/CloudFront |  |
   | クラウド/インフラ | AWS/RDS |  |
   | クラウド/インフラ | AWS/Route 53 |  |
   | クラウド/インフラ | AWS/CostExplorer |  |
   | サーバー | Nginx | 1.17.7 |
   | サーバー | Gunicorn | 20.1.0 |
   
### 参考
###### plotly
```text
https://qiita.com/studio_haneya/items/b689b4c27acbd12a888d
```

###### user認証機能のバグ修正
```text
https://qlitre-weblog.com/cant-migrate-django-custom-user/
```

###### ユーザー認証機能の実装
```text
https://qiita.com/grv2688/items/a22df0c72e8a1ed10cb4
```

###### デプロイ
```text
https://zenn.dev/leon0305/articles/8518e520e3b5ca
https://zenn.dev/tmasuyama1114/articles/ec2-linux-git-install
```

###### static読み込めないエラーの解消
```text
https://zenn.dev/leon0305/articles/8518e520e3b5ca
https://qiita.com/saira/items/a1c565c4a2eace268a07
```

###### デプロイ（セキュリティー強化）
```text
https://qiita.com/sindicum/items/620ba2984b6729e3a576
https://qiita.com/Bashi50/items/d5bc47eeb9668304aaa2
```

###### 管理者サイト
```text
https://qiita.com/ryo-keima/items/2bb55c05a79929ec9e71
```

##### 画像処理
```text
https://qiita.com/sitar-harmonics/items/ac584f99043574670cf3
```

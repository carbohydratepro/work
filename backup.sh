#!/bin/bash

# 現在の日付を取得
DATE=$(date +%Y%m%d)

# バックアップファイルの名前を設定
BACKUP_FILE="/path/to/backup/directory/backup_$DATE.sql.gz"

# PostgreSQLのバックアップを取得
pg_dump -U [ユーザ名] -h [ホスト名] -d [データベース名] | gzip > $BACKUP_FILE

# バックアップファイルをS3にアップロード
aws s3 cp $BACKUP_FILE s3://[バケット名]/path/to/backup/

# 任意: 古いバックアップをローカルから削除
find /path/to/backup/directory/ -type f -mtime +7 -name "backup_*.sql.gz" -exec rm {} \;

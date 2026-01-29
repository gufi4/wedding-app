#!/bin/bash
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Использование: ./restore.sh <файл_бэкапа>"
    exit 1
fi

docker run --rm \
  -v wedding_bot-data:/data \
  -v $(pwd):/backup \
  alpine \
  sh -c "cp /backup/$BACKUP_FILE /data/wedding_bot.db"

echo "База восстановлена из $BACKUP_FILE"

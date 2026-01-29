#!/bin/bash
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

docker run --rm \
  -v wedding_bot-data:/data \
  -v $(pwd)/$BACKUP_DIR:/backup \
  alpine \
  sh -c "cp /data/wedding_bot.db /backup/wedding_bot_${DATE}.db"

echo "Бэкап создан: wedding_bot_${DATE}.db"

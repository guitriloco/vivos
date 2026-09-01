#!/bin/bash
# Configuration
BACKUP_DIR="/home/team/shared/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
CURRENT_BACKUP="$BACKUP_DIR/backup_$DATE"
RETENTION_DAYS=7

# Create backup directory
mkdir -p "$CURRENT_BACKUP"
echo "Starting backup at $DATE..."

# 1. Backup Team Database
DB_FILE="/home/team/.data/agent-team-45a20d5d.db"
if [ -f "$DB_FILE" ]; then
    cp "$DB_FILE" "$CURRENT_BACKUP/team-db.sqlite"
    echo "Team database backed up."
else
    echo "Warning: Team database file not found at $DB_FILE"
fi

# 2. Backup Monitoring Configs
mkdir -p "$CURRENT_BACKUP/monitoring"
cp -r /home/team/shared/monitoring/* "$CURRENT_BACKUP/monitoring/" 2>/dev/null
echo "Monitoring configurations backed up."

# 3. Backup Sample App Configs
mkdir -p "$CURRENT_BACKUP/sample-app"
cp -r /home/team/shared/sample-app/* "$CURRENT_BACKUP/sample-app/" 2>/dev/null
echo "Sample app configurations backed up."

# 4. Compress the backup
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" -C "$BACKUP_DIR" "backup_$DATE"
rm -rf "$CURRENT_BACKUP"
echo "Backup completed: $BACKUP_DIR/backup_$DATE.tar.gz"

# 5. Cleanup old backups
find "$BACKUP_DIR" -name "backup_*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete
echo "Old backups cleaned up (Retention: $RETENTION_DAYS days)."

#!/bin/bash

# backup_db.sh - Database backup script

set -e  # Exit immediately if a command exits with a non-zero status

# Define backup directory and filename
BACKUP_DIR="./backups"
BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +'%Y%m%d_%H%M%S').sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Database connection string
DATABASE_URL=${DATABASE_URL:-"sqlite:///mydatabase.db"}

# Check if the database is SQLite
if [[ $DATABASE_URL == sqlite* ]]; then
    echo "Backing up SQLite database..."
    cp "${DATABASE_URL:10}" "$BACKUP_FILE"
else
    echo "Backing up PostgreSQL database..."
    PGPASSWORD=$DB_PASSWORD pg_dump -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME > "$BACKUP_FILE"
fi

echo "Backup completed successfully! Backup file: $BACKUP_FILE"

#!/bin/bash
#
# A simple script to back up the application database.

APP_DIR="/opt/box_counter_system"
DB_FILE="${APP_DIR}/data/box_counter.db"
BACKUP_DIR="${APP_DIR}/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.db.gz"

echo "--- Starting Database Backup ---"
mkdir -p "${BACKUP_DIR}"

if [ ! -f "$DB_FILE" ]; then
    echo "Database file not found at ${DB_FILE}. Exiting."
    exit 1
fi

echo "Backing up ${DB_FILE} to ${BACKUP_FILE}..."
# Use the sqlite3 command-line tool to perform a safe online backup
sqlite3 "${DB_FILE}" ".backup '${BACKUP_DIR}/temp_backup.db'"
gzip -c "${BACKUP_DIR}/temp_backup.db" > "${BACKUP_FILE}"
rm "${BACKUP_DIR}/temp_backup.db"

echo "Backup complete: ${BACKUP_FILE}"

# Optional: Clean up old backups (e.g., keep the last 7)
echo "Cleaning up old backups..."
ls -t "${BACKUP_DIR}"/*.gz | tail -n +8 | xargs -r rm

echo "--- Backup Process Finished ---"

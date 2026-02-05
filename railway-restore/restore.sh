#!/bin/sh
set -e

echo "Starting database restore..."
echo "Database URL: ${DATABASE_URL}"

# Parse Railway's asyncpg URL to standard PostgreSQL format
# Convert postgresql+asyncpg:// to postgresql://
DB_URL=$(echo $DATABASE_URL | sed 's/postgresql+asyncpg/postgresql/')

echo "Parsed DB URL: ${DB_URL}"

# Wait for PostgreSQL to be ready
until pg_isready -d "$DB_URL"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

echo "PostgreSQL is ready. Starting restore..."

# Restore the database
pg_restore -d "$DB_URL" -v --clean --if-exists /tmp/sentiment_db_backup.dump

echo "Database restore completed successfully!"
echo "Row counts:"
psql "$DB_URL" -c "SELECT 'raw_texts' as table_name, COUNT(*) as count FROM raw_texts UNION ALL SELECT 'sentiment_scores', COUNT(*) FROM sentiment_scores;"

# Keep container running so you can see the logs
echo "Restore complete. Container will exit in 60 seconds..."
sleep 60

# Railway Database Restore Service

This is a one-time service to restore the full database to Railway PostgreSQL.

## Contents

- `Dockerfile` - PostgreSQL container with restore script
- `restore.sh` - Script that performs the pg_restore
- `sentiment_db_backup.dump` - 525MB compressed database backup (2.66M texts)

## How to Deploy

### Option 1: Railway CLI (Recommended)

```bash
cd railway-restore

# Deploy to Railway
railway up

# This creates a new service in your Railway project
# The service will automatically:
# 1. Build the Docker image with the database dump
# 2. Run the restore script using the internal DATABASE_URL
# 3. Restore all 2.66M texts and sentiment scores
# 4. Print verification row counts
# 5. Exit after 60 seconds
```

### Option 2: Railway Dashboard

1. Go to Railway Dashboard → Your Project
2. Click "New Service" → "Empty Service"
3. Name it "database-restore" (temporary)
4. Connect this `railway-restore` directory
5. Railway will detect the Dockerfile and build it
6. Set environment variable: `DATABASE_URL` = (link to PostgreSQL service)
7. Deploy and watch logs for restore progress

## What It Does

1. **Waits for PostgreSQL** - Ensures database is ready
2. **Runs pg_restore** - Restores full 2.3GB database
   - `--clean` - Drops existing tables first
   - `--if-exists` - Won't error if tables don't exist
   - `-v` - Verbose output for monitoring
3. **Verifies** - Prints row counts after restore
4. **Exits** - Container stops after 60 seconds

## Expected Output

```
Starting database restore...
Database URL: postgresql://postgres:****@postgres.railway.internal:5432/railway
Parsed DB URL: postgresql://postgres:****@postgres.railway.internal:5432/railway
Waiting for PostgreSQL to be ready...
PostgreSQL is ready. Starting restore...
pg_restore: processing data for table "public.raw_texts"
pg_restore: processing data for table "public.sentiment_scores"
...
Database restore completed successfully!
Row counts:
  table_name    |  count
----------------+---------
 raw_texts      | 2657261
 sentiment_scores | 2657260
Restore complete. Container will exit in 60 seconds...
```

## After Restore

1. **Verify** - Check Railway PostgreSQL service shows increased storage usage (~2.3GB)
2. **Test API** - Hit your backend endpoints to verify data is accessible
3. **Test Frontend** - Visit live site and check dashboard loads with full data
4. **Remove Service** - Delete the "database-restore" service from Railway (no longer needed)

## Troubleshooting

**Error: "database does not exist"**
- Railway PostgreSQL should have a default "railway" database
- Check DATABASE_URL environment variable is correctly linked

**Error: "out of storage"**
- Verify you upgraded Railway PostgreSQL plan to handle 2.3GB
- Current dump is 525MB compressed, expands to 2.3GB

**Restore seems slow**
- Normal! 2.66M rows takes 5-10 minutes to restore
- Watch the logs for progress: "processing data for table..."

**Error: "permission denied"**
- Ensure DATABASE_URL is linked to the PostgreSQL service
- Railway should auto-inject this variable

## Estimated Time

- **Build**: 2-3 minutes (includes uploading 525MB dump)
- **Restore**: 5-10 minutes (depending on Railway's infrastructure)
- **Total**: 7-13 minutes

## Storage Requirements

- **Source dump**: 525MB (in this directory)
- **Railway build**: ~600MB (temporary, for building image)
- **Database after restore**: 2.3GB (permanent in PostgreSQL)

---

**Note**: This is a one-time operation. After successful restore, delete this service from Railway to avoid unnecessary resource usage.

# Railway Sentiment Indices Restore Service

This service restores the historical `sentiment_indices` data (aggregated daily sentiment scores) to Railway PostgreSQL.

## What It Does

- Loads 662 historical sentiment index records from 2016-2026
- Deletes existing aggregated data (source IS NULL) to avoid duplicates
- Inserts historical data for all asset classes (equity, crypto, forex, commodity)
- Verifies the restoration with counts by asset class

## How to Deploy

### Using Railway CLI

```bash
cd railway-restore-indices
railway up
```

The service will:
1. Build the Docker image with the JSON data file (395KB)
2. Connect to your Railway PostgreSQL database
3. Clear existing aggregated sentiment indices
4. Insert 662 historical records
5. Print verification results
6. Exit after 30 seconds

### Using Railway Dashboard

1. Go to Railway Dashboard → Your Project
2. Click "New Service" → "Empty Service"
3. Name it "restore-indices" (temporary)
4. Connect this `railway-restore-indices` directory
5. Railway will detect the Dockerfile and build it
6. Set environment variable: `DATABASE_URL` = (link to PostgreSQL service)
7. Deploy and watch logs

## Expected Output

```
Waiting for PostgreSQL to be ready...
PostgreSQL is ready!
Loading sentiment indices data...
Loaded 662 records
Date range: 2016-02-03T00:00:00+00:00 to 2026-01-31T00:00:00+00:00
Current sentiment_indices records (source IS NULL): 4
Clearing existing aggregated sentiment indices...
Deleted 4 existing records
Inserting 662 records...
Data inserted successfully!

Verification - Records by asset class:
  commodity: 81 records from 2021-01-28 to 2026-01-30
  crypto: 137 records from 2021-01-28 to 2026-01-31
  equity: 329 records from 2016-02-03 to 2026-01-30
  forex: 115 records from 2021-01-28 to 2026-01-30

Total records: 662
Date range: 2016-02-03 to 2026-01-31

✅ Sentiment indices restoration completed successfully!

Container will exit in 30 seconds...
```

## After Restoration

1. **Test API** - Visit: `https://sentiment-regime-detector.up.railway.app/api/v1/sentiment/cross-asset/history?days=90`
2. **Test Frontend** - Check the "Cross-Asset Sentiment History" chart shows 90 days of data
3. **Remove Service** - Delete the "restore-indices" service from Railway (no longer needed)

## Data Structure

The JSON file contains 662 records with fields:
- `id`, `asset_class`, `source`, `period_start`, `period_end`
- `granularity`, `mean_compound`, `std_compound`, `sample_count`
- `positive_ratio`, `negative_ratio`, `sentiment_momentum`, `sentiment_acceleration`
- `created_at`, `updated_at`

All records have `source IS NULL` (aggregated data, not source-specific).

## Storage Requirements

- **JSON file**: 395KB (compact)
- **Docker image**: ~300MB (Python + dependencies)
- **Database impact**: Minimal (662 records)

## Estimated Time

- **Build**: 1-2 minutes
- **Restore**: <30 seconds (662 records is fast)
- **Total**: 2-3 minutes

---

**Note**: This is a one-time operation. After successful restore, delete this service from Railway.

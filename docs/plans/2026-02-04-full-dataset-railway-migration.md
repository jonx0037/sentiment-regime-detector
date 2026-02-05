# Full Dataset Migration to Railway PostgreSQL

**Date:** February 4, 2026
**Author:** Jonathan Rocha
**Status:** In Progress
**Priority:** Critical - Required for production deployment

---

## Executive Summary

This document outlines the strategy for migrating the full historical dataset (281K texts, 277K sentiment scores) from local PostgreSQL development environment to Railway's production PostgreSQL instance. The live site currently runs with sample data (~10K texts) and needs the complete dataset to provide accurate historical analysis and regime detection.

**Timeline:** 30-45 minutes
**Risk Level:** Low (non-destructive, rollback available)
**Dependencies:** Railway CLI, PostgreSQL client tools

---

## Background & Context

### Current State

- **Local Development:** Full dataset (281,251 texts, 277,721 sentiment scores)
- **Production (Railway):** Sample dataset only (~10K texts)
- **Live Site:** https://sentiment-regime-detector.vercel.app (functional but limited data)
- **Database:** Railway PostgreSQL with internal passwordless authentication

### Why This Matters

1. **Academic Credibility:** Paper promises live deployment with full historical data
2. **Demo Quality:** March 20 presentation needs comprehensive historical analysis
3. **Validation:** Full dataset proves system scalability and production readiness
4. **Timeline:** 2 weeks until Draft-2, need production system finalized

### Decision Rationale

- **High confidence** in dataset quality (122 passing tests, validated locally)
- **Prioritize deployment** over additional backtesting at this stage
- **pg_dump/pg_restore** chosen as industry-standard migration approach

---

## Technical Approach

### Migration Strategy: Direct PostgreSQL Export/Import

We use PostgreSQL's native backup and restore tools:

- **`pg_dump`** - Exports local database to compressed binary format
- **Railway CLI** - Creates temporary secure proxy to production database
- **`pg_restore`** - Imports data through proxy into Railway PostgreSQL

### Why This Approach?

| Criteria | Rationale |
|----------|-----------|
| **Data Integrity** | Preserves all foreign keys, indexes, constraints |
| **Performance** | Faster than row-by-row inserts (2-5 min vs hours) |
| **Atomicity** | All-or-nothing operation, clean failure handling |
| **Safety** | Railway's internal auth unchanged, local DB untouched |
| **Simplicity** | Standard approach, well-documented, proven |

### Alternative Approaches Considered

1. **CSV Export/Import** - More control but slower, risk of encoding issues
2. **Run Pipeline Scripts on Railway** - Reproducible but time-consuming (hours)
3. **Manual SQL INSERT statements** - Too slow for 281K records

---

## Implementation Plan

### Phase 1: Database Export (5-10 minutes)

#### 1.1 Check Local Database Size

```bash
psql -U postgres -d sentiment_db -c "
  SELECT pg_size_pretty(pg_database_size('sentiment_db'));
"
```

**Expected:** ~100-500MB (depends on indexes, historical data)

#### 1.2 Verify Table Counts Before Export

```bash
psql -U postgres -d sentiment_db -c "
  SELECT
    'texts' as table_name, COUNT(*) as count FROM texts
  UNION ALL
  SELECT 'sentiment_scores', COUNT(*) FROM sentiment_scores
  UNION ALL
  SELECT 'backtest_results', COUNT(*) FROM backtest_results
  UNION ALL
  SELECT 'regime_classifications', COUNT(*) FROM regime_classifications;
"
```

**Expected counts:**
- texts: ~281,251
- sentiment_scores: ~277,721
- backtest_results: ~dozens (depends on backtests run)
- regime_classifications: ~varies

#### 1.3 Export Database

```bash
# Compressed binary format (recommended)
pg_dump -U postgres -d sentiment_db -F c -f sentiment_db_backup.dump

# Verify dump file created
ls -lh sentiment_db_backup.dump
```

**Output:** `sentiment_db_backup.dump` file (50-150MB compressed)

**If issues occur:**
- Use plain SQL format: `pg_dump -U postgres -d sentiment_db -f sentiment_db_backup.sql`
- Check disk space: `df -h`
- Verify PostgreSQL running: `pg_isready`

---

### Phase 2: Railway CLI Setup (5 minutes)

#### 2.1 Install Railway CLI (if needed)

```bash
# macOS
brew install railway

# or via npm
npm i -g @railway/cli
```

#### 2.2 Authenticate with Railway

```bash
railway login
```

Opens browser for authentication. Should show: "Successfully logged in!"

#### 2.3 Link to Project

```bash
cd /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone
railway link
```

Select your sentiment-regime-detector project when prompted.

#### 2.4 Verify Connection

```bash
railway status
```

Should display project name, environment, and connected services.

---

### Phase 3: Database Restore (10-15 minutes)

#### 3.1 Start Railway PostgreSQL Proxy

```bash
railway connect postgres
```

**Expected output:**
```
--> Connecting to postgres...
--> Running your service at localhost:5432
```

**Important:** Keep this terminal window open during restore!

#### 3.2 Restore Database (in new terminal)

```bash
# Navigate to backup location
cd /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone

# Restore via proxy
pg_restore -h localhost -p 5432 -U postgres -d railway -v sentiment_db_backup.dump
```

**Flags explained:**
- `-h localhost -p 5432`: Connect through Railway CLI proxy
- `-U postgres`: PostgreSQL username (Railway default)
- `-d railway`: Target database name
- `-v`: Verbose output (shows progress)

**Expected duration:** 2-5 minutes for 281K texts

**Progress indicators:**
```
pg_restore: processing data for table "public.texts"
pg_restore: processing data for table "public.sentiment_scores"
pg_restore: creating INDEX "idx_texts_created_at"
...
```

#### 3.3 If Restore Fails

**Error: "database railway does not exist"**
```bash
# Create database first
psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE railway;"
```

**Error: "table already exists"**
```bash
# Use --clean flag to drop existing tables first
pg_restore -h localhost -p 5432 -U postgres -d railway -v --clean sentiment_db_backup.dump
```

**Error: connection refused**
- Verify Railway CLI proxy is running in other terminal
- Check `railway status` shows correct project

---

### Phase 4: Verification (10-15 minutes)

#### 4.1 Verify Row Counts Match

```bash
# Connect via proxy
psql -h localhost -p 5432 -U postgres -d railway

# Run verification queries
SELECT
  'texts' as table_name, COUNT(*) as count FROM texts
UNION ALL
SELECT 'sentiment_scores', COUNT(*) FROM sentiment_scores
UNION ALL
SELECT 'backtest_results', COUNT(*) FROM backtest_results
UNION ALL
SELECT 'regime_classifications', COUNT(*) FROM regime_classifications;
```

**Compare to local counts from Phase 1.2**

#### 4.2 Verify Data Quality

```bash
# Check date range (should span years)
SELECT
  MIN(created_at) as earliest_text,
  MAX(created_at) as latest_text,
  COUNT(*) as total_texts
FROM texts;

# Expected: earliest ~2008-2010, latest ~2024-2025

# Check asset class distribution
SELECT asset_class, COUNT(*)
FROM sentiment_scores
GROUP BY asset_class
ORDER BY COUNT(*) DESC;

# Expected: equities, crypto, forex, commodities all present

# Verify sentiment scores are reasonable
SELECT
  asset_class,
  AVG(sentiment_score) as avg_sentiment,
  STDDEV(sentiment_score) as stddev_sentiment,
  MIN(sentiment_score) as min_sentiment,
  MAX(sentiment_score) as max_sentiment
FROM sentiment_scores
GROUP BY asset_class;

# Expected: scores between -1 and 1, reasonable distributions
```

#### 4.3 Test API Endpoints

```bash
# Wait a moment for Railway to detect database changes, then test

# Test health endpoint
curl https://sentiment-regime-detector-production.up.railway.app/health

# Test sentiment aggregate
curl https://sentiment-regime-detector-production.up.railway.app/api/v1/sentiment/aggregate

# Test regime detection
curl https://sentiment-regime-detector-production.up.railway.app/api/v1/regime/current

# All should return 200 OK with data
```

#### 4.4 Frontend Testing

1. **Visit live site:** https://sentiment-regime-detector.vercel.app
2. **Check dashboard loads** - should show aggregate sentiment
3. **Test date range selector:**
   - Select "2008 Financial Crisis" (Sep 2008 - Mar 2009)
   - Should show meaningful sentiment data (not empty)
4. **Test regime detector:**
   - Should classify current regime with VIX/CISS data
5. **Check asset class breakdown:**
   - All asset classes should show substantial data
6. **Test export functionality:**
   - Click "Export Data" button
   - Verify CSV/JSON downloads work
7. **Test multiple timeframes:**
   - 2020 COVID crash (Feb-Mar 2020)
   - Recent data (2024-2025)
   - All should have data

#### 4.5 Performance Checks

Monitor Railway dashboard after migration:

- **Database size:** Should be under 512MB (free tier limit)
- **Query performance:** Dashboard queries should complete < 2 seconds
- **API response times:** Check Railway logs for endpoint latency
- **Memory usage:** Backend API should stay within Railway plan limits

**If performance degrades:**
- Check for missing indexes
- Review slow query logs in Railway
- Consider upgrading Railway plan if needed

---

## Success Criteria

### ✅ Migration Successful If:

1. Row counts match local database (±1% acceptable)
2. Date ranges span full historical period (2008-2025)
3. All asset classes have substantial data (>1000 records each)
4. API endpoints return 200 OK with full data
5. Frontend dashboard shows complete historical data
6. No errors in Railway application logs
7. Database size under Railway plan limits
8. Query performance acceptable (<2s for dashboard)

### ❌ Rollback If:

1. Row counts significantly different (>10% variance)
2. Data quality issues (NULL values, wrong ranges)
3. API endpoints returning errors or empty results
4. Frontend fails to load or shows errors
5. Database exceeds storage limits
6. Critical performance degradation

---

## Rollback Plan

If migration fails or causes issues:

### Option 1: Railway Database Snapshot Restore

```bash
# Railway keeps automatic backups
# Go to Railway dashboard → PostgreSQL → Backups
# Select snapshot before migration → Restore
```

### Option 2: Re-import Sample Data

```bash
# Export current sample data first (as backup)
pg_dump -h localhost -p 5432 -U postgres -d railway -F c -f railway_sample_backup.dump

# If needed, restore sample data
pg_restore -h localhost -p 5432 -U postgres -d railway --clean railway_sample_backup.dump
```

### Option 3: Retry Migration

```bash
# Clear Railway database
psql -h localhost -p 5432 -U postgres -d railway -c "
  DROP SCHEMA public CASCADE;
  CREATE SCHEMA public;
"

# Re-run pg_restore from Phase 3
pg_restore -h localhost -p 5432 -U postgres -d railway -v sentiment_db_backup.dump
```

**Note:** Local database remains untouched - can retry as many times as needed.

---

## Post-Migration Tasks

### Immediate (After Verification Passes)

- [ ] Stop Railway CLI proxy (`Ctrl+C` in terminal)
- [ ] Document actual row counts in this file
- [ ] Take screenshots of live dashboard for paper
- [ ] Update README.md with "full dataset deployed" status
- [ ] Commit this documentation to git
- [ ] Monitor Railway logs for 24 hours for any issues

### Short-term (This Week)

- [ ] Monitor Railway database metrics (size, query performance)
- [ ] Test frontend performance with multiple concurrent users
- [ ] Consider COVID-19 crash backtest (optional, if time permits)
- [ ] Update project documentation with production URLs

### Deferred (Post-Draft-2)

- [ ] Set up live API integration (Reddit, Twitter, News)
- [ ] Additional backtests (2022 crypto winter, 2024-2025)
- [ ] Advanced analysis (SHAP/LIME explainability)

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Database storage exceeds limit | Low | Medium | Monitor size during restore, can selectively exclude tables |
| Performance degradation | Low | Medium | Verify indexes restored, upgrade Railway plan if needed |
| Data corruption during transfer | Very Low | High | Verify checksums, test data quality queries |
| Railway internal auth breaks | Very Low | High | Not touching auth config, only restoring data |
| Frontend breaks with full data | Low | Medium | Full verification checklist, easy rollback available |
| Migration takes longer than expected | Low | Low | Non-blocking, can retry anytime |

**Overall Risk Level: LOW** - Standard database migration, proven approach, non-destructive to local environment.

---

## Estimated Timeline

| Phase | Duration | Can Parallelize? |
|-------|----------|------------------|
| Database Export | 5-10 min | No |
| Railway CLI Setup | 5 min | No (but one-time) |
| Database Restore | 10-15 min | No |
| Verification | 10-15 min | Partially (SQL + Frontend) |
| **Total** | **30-45 min** | |

**Best time to execute:** Off-peak hours (evening) to avoid disrupting live site users (if any).

---

## Lessons Learned (Post-Execution)

_To be filled in after migration completes:_

### What Went Well

-

### Challenges Encountered

-

### Actual vs Estimated Timeline

-

### Recommendations for Future Migrations

-

---

## References

- [Railway PostgreSQL Documentation](https://docs.railway.app/databases/postgresql)
- [Railway CLI Reference](https://docs.railway.app/develop/cli)
- [PostgreSQL pg_dump Documentation](https://www.postgresql.org/docs/current/app-pgdump.html)
- [PostgreSQL pg_restore Documentation](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [Project DEPLOYMENT.md](../DEPLOYMENT.md)

---

## Approval & Sign-off

**Design Approved:** February 4, 2026
**Ready for Execution:** ✅ Yes
**Blockers:** None
**Go/No-Go Decision:** GO

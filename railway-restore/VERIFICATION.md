# Database Restore Verification Checklist

After the restore service completes, follow these steps to verify the migration was successful.

## 1. Check Railway Logs

In Railway Dashboard:
1. Go to your project → "database-restore" service
2. Click on "Deployments" → Latest deployment
3. View logs - should see:
   ```
   Database restore completed successfully!
   Row counts:
     table_name    |  count
   ----------------+---------
    raw_texts      | 2657261
    sentiment_scores | 2657260
   ```

## 2. Verify Database Size

1. Go to Railway Dashboard → PostgreSQL service
2. Check "Metrics" tab
3. Storage usage should show ~2.3GB (up from previous small sample)

## 3. Test Backend API Endpoints

```bash
# Health check
curl https://sentiment-regime-detector-production.up.railway.app/health

# Get sentiment aggregate (should return data for all asset classes)
curl https://sentiment-regime-detector-production.up.railway.app/api/v1/sentiment/aggregate

# Get current regime
curl https://sentiment-regime-detector-production.up.railway.app/api/v1/regime/current

# Get historical sentiment for a specific period
curl "https://sentiment-regime-detector-production.up.railway.app/api/v1/sentiment/historical?start_date=2020-02-01&end_date=2020-03-31"
```

Expected responses:
- All should return 200 OK
- Aggregate should show meaningful sentiment values
- Historical queries should return data for requested periods

## 4. Test Frontend Dashboard

Visit: https://sentiment-regime-detector.vercel.app

### Dashboard Tests:

1. **Main Dashboard Loads**
   - Should show aggregate sentiment chart
   - All asset classes visible (equities, crypto, forex, commodities)
   - Recent data points displayed

2. **Date Range Selector**
   - Select "2008 Financial Crisis" (Sep 2008 - Mar 2009)
   - Should display historical sentiment data
   - Chart should show crisis-period patterns

3. **Regime Detector**
   - Current regime should be classified (Normal/Stress/Crisis)
   - VIX and CISS values displayed
   - Confidence score shown

4. **Asset Class Breakdown**
   - Click on each asset class tab
   - Should show time-series data
   - No empty states or "no data" messages

5. **Export Functionality**
   - Click "Export Data" button
   - Select CSV or JSON format
   - Download should contain full dataset

### Historical Period Tests:

Test these specific periods to verify full historical coverage:

| Period | Date Range | Expected Behavior |
|--------|------------|-------------------|
| 2008 GFC | Sep 2008 - Mar 2009 | High volatility, negative sentiment |
| 2020 COVID | Feb 2020 - Apr 2020 | Sharp sentiment drop, VIX spike |
| 2022 Crypto Winter | May 2022 - Jul 2022 | Crypto-specific stress |
| Recent Data | Jan 2025 - Feb 2025 | Current market sentiment |

## 5. Database Query Verification

If you have access to Railway PostgreSQL (via CLI or dashboard):

```sql
-- Verify row counts
SELECT
  'raw_texts' as table_name, COUNT(*) as count FROM raw_texts
UNION ALL
SELECT 'sentiment_scores', COUNT(*) FROM sentiment_scores
UNION ALL
SELECT 'market_data', COUNT(*) FROM market_data
UNION ALL
SELECT 'stress_indices', COUNT(*) FROM stress_indices;

-- Expected:
-- raw_texts: 2,657,261
-- sentiment_scores: 2,657,260
-- market_data: ~139,909
-- stress_indices: ~12,029

-- Verify date range
SELECT
  MIN(created_at) as earliest,
  MAX(created_at) as latest,
  COUNT(*) as total
FROM raw_texts;

-- Expected:
-- earliest: ~2008-2010 (early Kaggle datasets)
-- latest: ~2024-2025 (recent data)
-- total: 2,657,261

-- Verify asset class distribution
SELECT
  asset_class,
  COUNT(*) as count,
  ROUND(AVG(sentiment_score)::numeric, 3) as avg_sentiment
FROM sentiment_scores
GROUP BY asset_class
ORDER BY count DESC;

-- Expected:
-- All asset classes present (equities, crypto, forex, commodities)
-- Reasonable sentiment averages (between -1 and 1)
-- Substantial counts for each class

-- Check for data quality
SELECT
  COUNT(*) as total,
  COUNT(*) FILTER (WHERE sentiment_score IS NULL) as null_scores,
  COUNT(*) FILTER (WHERE sentiment_score < -1 OR sentiment_score > 1) as invalid_scores
FROM sentiment_scores;

-- Expected:
-- null_scores: 0 (or very few)
-- invalid_scores: 0
```

## 6. Performance Verification

Monitor Railway metrics for 24 hours:

1. **API Response Times**
   - Dashboard queries: < 2 seconds
   - Historical queries: < 5 seconds
   - No timeouts or 502 errors

2. **Database Performance**
   - Query times in Railway logs
   - No slow query warnings
   - CPU/Memory within plan limits

3. **Storage**
   - Database: ~2.3GB stable
   - No unexpected growth
   - Backups running successfully

## Success Criteria

✅ **Migration is successful if:**

- [ ] Restore logs show completion without errors
- [ ] Row counts match local database (2.66M texts)
- [ ] Database size shows ~2.3GB in Railway
- [ ] All API endpoints return 200 OK with data
- [ ] Frontend dashboard loads and displays full historical data
- [ ] Date range selector works for all periods (2008-2025)
- [ ] No NULL or invalid sentiment scores
- [ ] Performance acceptable (queries < 2s)

❌ **Rollback if:**

- Restore failed with errors
- Row counts significantly different (>10% variance)
- Data quality issues (many NULLs, invalid ranges)
- Frontend shows errors or empty states
- API endpoints timing out
- Database exceeds storage plan limits

## Troubleshooting

### Issue: Frontend still shows sample data

**Solution:**
1. Check Railway backend logs - might be caching
2. Restart Railway backend service
3. Clear browser cache and reload frontend
4. Verify API endpoints return full data (curl test)

### Issue: Some historical periods have no data

**Solution:**
1. Check date ranges in database:
   ```sql
   SELECT DATE_TRUNC('month', created_at) as month, COUNT(*)
   FROM raw_texts
   GROUP BY month
   ORDER BY month;
   ```
2. Verify specific period has texts in source data

### Issue: API queries are slow

**Solution:**
1. Check for missing indexes:
   ```sql
   SELECT schemaname, tablename, indexname
   FROM pg_indexes
   WHERE schemaname = 'public'
   ORDER BY tablename;
   ```
2. Verify indexes on:
   - `raw_texts.created_at`
   - `sentiment_scores.asset_class`
   - `sentiment_scores.created_at`
3. If missing, restore should have recreated them automatically

### Issue: Out of storage on Railway

**Solution:**
1. Verify you upgraded to appropriate plan
2. Check database size:
   ```sql
   SELECT pg_size_pretty(pg_database_size('railway'));
   ```
3. If needed, upgrade to higher storage tier
4. Consider archiving old data if not needed

## Post-Verification Tasks

After successful verification:

- [ ] Document actual row counts in migration plan
- [ ] Take screenshots of live dashboard for paper
- [ ] Update README with "full dataset deployed" badge
- [ ] Delete "database-restore" service from Railway (no longer needed)
- [ ] Commit migration documentation to git
- [ ] Monitor Railway logs for 24-48 hours
- [ ] Set up automated database backups in Railway

## Monitoring Schedule

**First 24 hours:**
- Check logs every 2 hours
- Monitor API response times
- Watch for error patterns

**First week:**
- Daily dashboard check
- Weekly performance review
- Storage growth monitoring

**Ongoing:**
- Railway should auto-backup database
- Set up alerts for API errors
- Monitor storage approaching limits

---

**Note:** Keep local database backup (`sentiment_db_backup.dump`) until you've verified production is stable for at least 1 week.

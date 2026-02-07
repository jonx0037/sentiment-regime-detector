# Importing Data to Railway Production Database

## Issue

The `DATABASE_URL` environment variable uses `postgres.railway.internal` which is only accessible from within Railway's network. We need the public connection URL to import data from your local machine.

## Solution Options

### Option 1: Get Public Database URL from Railway Dashboard (Fastest)

1. **Go to Railway Dashboard**:
   - Visit: <https://railway.app>
   - Open your `sentiment-regime-detector` project

2. **Find Postgres Service**:
   - Look for the Postgres database service/plugin in your project
   - Click on it to open the service details

3. **Get Public Connection URL**:
   - Click the "Connect" or "Variables" tab
   - Look for **"TCP Proxy"** or **"Public URL"** section
   - Copy the connection string that looks like:

     ```
     postgresql://user:pass@containers-us-west-XXX.railway.app:5432/railway
     ```

4. **Run Import with Public URL**:

   ```bash
   # Set the public database URL
   export DATABASE_URL="<paste-public-url-here>"

   # Run the import
   python scripts/admin/import_ciss_production.py
   ```

### Option 2: Create a Railway Job/Service (More Complex)

Create a one-time service that runs the import from within Railway:

1. Create `railway-import.toml`:

   ```toml
   [build]
   builder = "NIXPACKS"

   [deploy]
   startCommand = "python scripts/admin/import_ciss_production.py"
   restartPolicyType = "NEVER"
   ```

2. Deploy as a one-time job:

   ```bash
   railway up --detach
   ```

### Option 3: Minimal Data Seed (Temporary)

If you just need to test the explainability features quickly, create a minimal dataset:

```bash
# Create minimal CISS data (last 30 days only)
python -c "
import pandas as pd
from datetime import datetime, timedelta

# Create 30 days of sample CISS data
dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
ciss_values = [0.15, 0.16, 0.14, 0.17, 0.15, 0.18, 0.16, 0.15,
               0.17, 0.16, 0.19, 0.18, 0.17, 0.16, 0.15, 0.18,
               0.17, 0.16, 0.19, 0.18, 0.17, 0.16, 0.18, 0.17,
               0.16, 0.19, 0.18, 0.17, 0.20, 0.19]

df = pd.DataFrame({'date': dates, 'value': ciss_values})
df.to_csv('minimal_ciss.csv', index=False)
print('Created minimal_ciss.csv')
"
```

Then import this minimal dataset using the public URL.

## Recommended: Option 1

The fastest way is **Option 1** - getting the public database URL takes ~2 minutes and allows you to import the full historical dataset (12,029 CISS observations from 1980-2026).

Once you have the public URL, run:

```bash
export DATABASE_URL="postgresql://user:pass@containers-us-west-XXX.railway.app:5432/railway"
python scripts/admin/import_ciss_production.py
```

## After Import

Test that data was imported:

```bash
# Count CISS records
railway run python -c "
import asyncio
from sqlalchemy import text, create_engine

url = '${DATABASE_URL}'.replace('+asyncpg', '')
engine = create_engine(url)

with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM stress_indices'))
    print(f'CISS records in production: {result.scalar()}')
"
```

Then test the explainability endpoint:

```bash
curl https://sentiment-regime-detector-production.up.railway.app/api/v1/explainability/current
```

If you see actual data (not 500 error), the buttons will work! 🎉

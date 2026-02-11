FROM python:3.11-slim

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Install Python dependencies  
RUN pip install --no-cache-dir psycopg2-binary pandas

# Copy data and script
COPY daily_sentiment.csv /app/daily_sentiment.csv
COPY ecb_ciss_daily.csv /app/ecb_ciss_daily.csv
COPY vix_daily.csv /app/vix_daily.csv
COPY feature_matrix.csv /app/feature_matrix.csv
COPY seed_dashboard.py /app/seed_dashboard.py

WORKDIR /app

CMD ["python", "/app/seed_dashboard.py"]

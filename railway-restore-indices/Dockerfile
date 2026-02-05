FROM python:3.11-slim

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir psycopg2-binary

# Copy data and script
COPY sentiment_indices_export.json /app/sentiment_indices_export.json
COPY restore_indices.py /app/restore_indices.py

# Make script executable
RUN chmod +x /app/restore_indices.py

# Set working directory
WORKDIR /app

# Run restore script
CMD ["python", "/app/restore_indices.py"]

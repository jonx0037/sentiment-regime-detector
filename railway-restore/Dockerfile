FROM postgres:15-alpine

# Install necessary tools
RUN apk add --no-cache curl

# Download the database dump from GitHub Release
RUN curl -L https://github.com/jonx0037/sentiment-regime-detector/releases/download/v0.1.0-db-migration/sentiment_db_backup.dump \
    -o /tmp/sentiment_db_backup.dump

# Create restore script
COPY restore.sh /restore.sh
RUN chmod +x /restore.sh

CMD ["/restore.sh"]

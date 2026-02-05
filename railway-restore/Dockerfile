FROM postgres:15-alpine

# Install necessary tools
RUN apk add --no-cache curl

# Copy the database dump
COPY sentiment_db_backup.dump /tmp/sentiment_db_backup.dump

# Create restore script
COPY restore.sh /restore.sh
RUN chmod +x /restore.sh

CMD ["/restore.sh"]

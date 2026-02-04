#!/bin/bash
# Start both backend and frontend development servers

set -e

PROJECT_ROOT="/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone"

echo "======================================================================="
echo "SENTIMENT REGIME DETECTOR - Development Server Startup"
echo "======================================================================="
echo ""

# Check if Docker is running
if ! docker ps &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check database containers
echo "Checking database containers..."
if ! docker ps | grep -q "sentiment-db"; then
    echo "⚠️  Database containers not running. Starting them..."
    cd "$PROJECT_ROOT"
    docker-compose -f docker-compose.dev.yml up -d
    sleep 3
fi
echo "✅ Database containers are running"
echo ""

# Function to start backend
start_backend() {
    echo "Starting FastAPI backend on http://localhost:8000..."
    cd "$PROJECT_ROOT"
    source .venv/bin/activate
    PYTHONPATH="$PROJECT_ROOT/src" uvicorn sentiment_detector.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload \
        --reload-exclude '.venv/*'
}

# Function to start frontend
start_frontend() {
    echo "Starting Next.js frontend on http://localhost:3000..."
    cd "$PROJECT_ROOT/frontend"
    npm run dev
}

# Trap to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down development servers..."
    kill 0
}
trap cleanup EXIT INT TERM

# Start backend in background
start_backend &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend (this will run in foreground)
start_frontend

# Wait for all background processes
wait

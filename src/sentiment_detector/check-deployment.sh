#!/bin/bash
# Monitor Railway deployment status

echo "🔍 Checking Railway Deployment Status..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check health endpoint
echo -n "Health Check: "
HEALTH=$(curl -s https://sentiment-regime-detector-production.up.railway.app/api/v1/health | jq -r '.status' 2>/dev/null)
if [ "$HEALTH" = "healthy" ]; then
    echo "✅ Healthy"
else
    echo "❌ Not responding"
    exit 1
fi

# Check explainability endpoint (NEW CODE)
echo -n "Explainability Endpoint: "
EXPLAIN=$(curl -s https://sentiment-regime-detector-production.up.railway.app/api/v1/explainability/events 2>/dev/null)
if echo "$EXPLAIN" | jq -e 'type == "array"' > /dev/null 2>&1; then
    COUNT=$(echo "$EXPLAIN" | jq 'length')
    echo "✅ Live! ($COUNT crisis events)"

    # Show sample data
    echo ""
    echo "📊 Sample Response:"
    echo "$EXPLAIN" | jq -r '.[0] | "  - \(.name) (\(.date))"' 2>/dev/null

    echo ""
    echo "🎉 DEPLOYMENT SUCCESSFUL!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Backend: https://sentiment-regime-detector-production.up.railway.app"
    echo "API Docs: https://sentiment-regime-detector-production.up.railway.app/docs"
    echo ""
    echo "✅ Ready for frontend deployment!"
    exit 0
else
    echo "⏳ Still deploying (endpoints return 404)"
    echo ""
    echo "Run this script again in a few minutes..."
    exit 1
fi

#!/bin/bash
# Check Vercel deployment status

echo "🔍 Checking Vercel Deployment..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Get Vercel domain from config
DOMAIN=$(grep -o 'sentiment-regime-detector[^"]*vercel\.app' /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone/frontend/.vercel/project.json 2>/dev/null || echo "sentiment-regime-detector.vercel.app")

echo "Domain: https://$DOMAIN"
echo ""

# Check if site is reachable
echo -n "Site Status: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN)
if [ "$STATUS" = "200" ]; then
    echo "✅ Live (HTTP $STATUS)"
    echo ""
    echo "🎉 Frontend deployed!"
    echo "Visit: https://$DOMAIN"
else
    echo "⏳ Deploying... (HTTP $STATUS)"
fi

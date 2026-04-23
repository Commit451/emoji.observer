#!/usr/bin/env bash
# update.sh — Scrape latest emojis from Unicode and rebuild the site
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== emoji.observer update ==="
echo ""

# 1. Scrape fresh emoji data
echo "1️⃣  Scraping emoji data from unicode.org..."
cd "$PROJECT_DIR"
python3 scripts/scrape-emojis.py

# 2. Rebuild static site (generates all emoji pages + sitemap)
echo ""
echo "2️⃣  Rebuilding site..."
npm run build

echo ""
echo "✅ Done! New pages generated in dist/"

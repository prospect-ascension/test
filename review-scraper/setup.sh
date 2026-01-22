#!/bin/bash
# Quick setup script for the review scraper

echo "=========================================="
echo "Review Scraper - Setup"
echo "=========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Install Playwright browsers
echo ""
echo "Installing Playwright Chromium browser..."
echo "(This may take a few minutes...)"
python3 -m playwright install chromium
if [ $? -eq 0 ]; then
    echo "✓ Playwright browser installed"
else
    echo "✗ Failed to install Playwright browser"
    exit 1
fi

# Create output directory
mkdir -p output
echo "✓ Output directory created"

echo ""
echo "=========================================="
echo "Setup complete! 🎉"
echo "=========================================="
echo ""
echo "To start scraping:"
echo "  python3 scrape_reviews.py"
echo ""
echo "For usage instructions, see USAGE.md"
echo ""

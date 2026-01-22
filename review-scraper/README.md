# Review Scraper

Fast scraper for Trustpilot, G2, and Capterra reviews.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run scraper
python scrape_reviews.py
```

## Usage

1. Run the script
2. Enter company names when prompted (comma-separated)
3. Reviews will be saved to `output/` directory as CSV files

## Output Files

- `output/trustpilot_reviews.csv`
- `output/g2_reviews.csv`
- `output/capterra_reviews.csv`
- `output/all_reviews.csv` (combined)

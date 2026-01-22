# Review Scraper

Fast, reliable scraper for Trustpilot, G2, and Capterra reviews using **direct URLs**.

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
cd review-scraper
pip install -r requirements.txt
python3 -m playwright install chromium
```

### 2. Configure Companies

Edit `companies.yaml` with your target companies and their review page URLs:

```yaml
companies:
  - name: YourCompany
    trustpilot: https://uk.trustpilot.com/review/yourcompany.com
    g2: https://www.g2.com/products/yourcompany/reviews
    capterra: https://www.capterra.co.uk/software/123456/yourcompany
```

Set any platform to `null` if the company doesn't have a page there.

### 3. Run the Scraper

```bash
python3 scrape_reviews.py
```

That's it! The scraper will:
- Read all companies from `companies.yaml`
- Scrape each platform sequentially
- Save results to CSV files in `output/` directory

## Output Files

All saved to `output/` directory:

- **`trustpilot_reviews.csv`** - All Trustpilot reviews
- **`g2_reviews.csv`** - All G2 reviews
- **`capterra_reviews.csv`** - All Capterra reviews
- **`all_reviews.csv`** - Combined dataset

## CSV Format

Each row contains:

| Column | Description |
|--------|-------------|
| `company` | Company name |
| `platform` | Review platform |
| `rating` | Star rating (1-5) |
| `title` | Review title |
| `content` | Full review text |
| `author` | Reviewer name |
| `date` | Review date (YYYY-MM-DD) |
| `verified` | Whether review is verified |
| `url` | Source URL |

## Why Direct URLs?

✅ **More reliable** - No search errors or wrong company matches
✅ **Faster** - Skips the search step entirely
✅ **More control** - You choose exactly which pages to scrape
✅ **Easier debugging** - If it fails, you know exactly where

## Configuration Options

### Change Scraping Limits

Edit these values in the scraper files:

**Trustpilot** (`scrapers/trustpilot.py` line 13):
```python
async def scrape_reviews(self, company_name: str, url: str, max_pages: int = 50):
```

**G2** (`scrapers/g2.py` line 13):
```python
async def scrape_reviews(self, company_name: str, url: str, max_reviews: int = 200):
```

**Capterra** (`scrapers/capterra.py` line 13):
```python
async def scrape_reviews(self, company_name: str, url: str, max_pages: int = 20):
```

### Add More Companies

Just add more entries to `companies.yaml`:

```yaml
companies:
  - name: Company1
    trustpilot: https://uk.trustpilot.com/review/company1.com
    g2: https://www.g2.com/products/company1/reviews
    capterra: https://www.capterra.co.uk/software/123456/company1

  - name: Company2
    trustpilot: https://uk.trustpilot.com/review/company2.com
    g2: null  # No G2 page
    capterra: https://www.capterra.co.uk/software/789012/company2
```

## Expected Performance

For the default 7 companies across 3 platforms:

- **Runtime**: 30-45 minutes
- **Expected reviews**: 3,000-8,000+ reviews
- **File size**: 5-15 MB total

## Finding Review URLs

### Trustpilot
1. Search for company on trustpilot.com
2. Click on their profile
3. Copy URL (format: `https://uk.trustpilot.com/review/companyname.com`)

### G2
1. Search for company on g2.com
2. Click on their product page
3. Add `/reviews` to the end of URL
4. Copy full URL (format: `https://www.g2.com/products/product-name/reviews`)

### Capterra
1. Search for company on capterra.com or capterra.co.uk
2. Click on their profile
3. Copy URL (format: `https://www.capterra.co.uk/software/123456/product-name`)

## Troubleshooting

### "No reviews found on page 1"

The website HTML might have changed. Check:
1. Does the URL load in your browser?
2. Are reviews visible on the page?
3. The CSS selectors may need updating (open an issue)

### "Failed to load page"

Network issue or blocked. Try:
1. Check your internet connection
2. Try the URL in a regular browser
3. The site may have anti-bot protection (use proxies)

### YAML parsing error

Check your `companies.yaml` syntax:
- Proper indentation (2 spaces)
- All URLs in quotes if they contain special characters
- Use `null` (not `None` or empty) for missing URLs

## Technical Details

- **Python 3.11+** with async/await
- **Playwright** for headless browser automation
- **Rate limiting**: 2-3 second delays between companies
- **Error handling**: Continues on individual failures
- **CSV export**: UTF-8 encoding for all languages

## Legal & Ethical

✅ Scraping publicly available reviews for research
✅ Respectful rate limiting built-in
✅ No PII collection beyond public review data
⚠️  Check each platform's ToS before large-scale scraping

---

**Need help?** Check `USAGE.md` for detailed instructions and troubleshooting.

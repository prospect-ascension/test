# Review Scraper - Usage Guide

## What This Does

Scrapes customer reviews from **Trustpilot**, **G2**, and **Capterra** for any list of companies you provide.

Perfect for competitive intelligence, market research, and analyzing customer sentiment at scale.

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
cd review-scraper
pip install -r requirements.txt
python3 -m playwright install chromium
```

### 2. Run the Scraper

```bash
python3 scrape_reviews.py
```

### 3. Enter Company Names

When prompted, enter comma-separated company names:

```
Companies: Wise, Revolut Business, Airwallex, WorldFirst, Payoneer
```

Or just press Enter to use the default list of 9 competitors:
- Wise
- Revolut Business
- Airwallex
- WorldFirst
- Payoneer
- Aspire
- Statrys
- OFX
- Currencycloud

### 4. Wait for Results

The scraper will:
- Find each company on all 3 platforms
- Scrape all available reviews (can be 100s or 1000s per company)
- Show progress in real-time
- Save results to CSV files

### 5. Get Your Data

All results saved to `output/` directory:

- **`trustpilot_reviews.csv`** - All Trustpilot reviews
- **`g2_reviews.csv`** - All G2 reviews
- **`capterra_reviews.csv`** - All Capterra reviews
- **`all_reviews.csv`** - Combined dataset

## CSV Output Format

Each row contains:

| Column | Description |
|--------|-------------|
| `company` | Company name |
| `platform` | Review platform (Trustpilot/G2/Capterra) |
| `rating` | Star rating (1-5) |
| `title` | Review title/headline |
| `content` | Full review text |
| `author` | Reviewer name |
| `date` | Review date (YYYY-MM-DD) |
| `verified` | Whether review is verified |
| `url` | Source URL |

## How It Works

### Trustpilot
- Uses browser automation (Playwright)
- Scrapes up to 50 pages per company (~1000 reviews)
- Extracts: rating, title, content, author, date, verification status
- **Speed**: ~2-3 minutes per company

### G2
- Uses browser automation with infinite scroll
- Loads up to 200 reviews per company (configurable)
- Extracts: rating, title, content, author, date
- **Speed**: ~3-5 minutes per company (slower due to JavaScript rendering)

### Capterra
- Uses browser automation with pagination
- Scrapes up to 20 pages per company
- Extracts: rating, title, content, author, date
- **Speed**: ~2-4 minutes per company

## Customization

### Scrape More/Fewer Reviews

Edit the scraper files to change limits:

**`scrapers/trustpilot.py`** - Line 62:
```python
async def scrape_reviews(self, company_name: str, max_pages: int = 50):
```

**`scrapers/g2.py`** - Line 60:
```python
async def scrape_reviews(self, company_name: str, max_reviews: int = 200):
```

**`scrapers/capterra.py`** - Line 59:
```python
async def scrape_reviews(self, company_name: str, max_pages: int = 20):
```

### Scrape Specific Platforms Only

Comment out platforms you don't need in `scrape_reviews.py`:

```python
# Skip G2 and Capterra
trustpilot_reviews = await scrape_trustpilot(company_names)
# g2_reviews = await scrape_g2(company_names)
# capterra_reviews = await scrape_capterra(company_names)
```

## Expected Results

For 9 companies across 3 platforms:

- **Total runtime**: 30-60 minutes
- **Expected reviews**: 3,000-10,000+ reviews
- **File sizes**: 5-20 MB total

## Troubleshooting

### "Could not find [Company] on [Platform]"

**Cause**: Company name doesn't match exactly

**Solutions**:
1. Try different variations: "Wise", "Wise.com", "Wise Payments"
2. Manually find the company URL and update the scraper
3. Some companies may not have pages on all platforms

### "Rate limited" or "Blocked"

**Cause**: Too many requests too fast

**Solutions**:
1. Increase delays between requests (edit `asyncio.sleep()` values)
2. Run fewer companies at once
3. Use a VPN or proxy

### "Browser failed to launch"

**Cause**: Playwright not installed properly

**Solution**:
```bash
python3 -m playwright install chromium
```

### CSV encoding issues

**Cause**: Special characters in reviews

**Solution**: Open CSV in Excel or Google Sheets (auto-detects UTF-8)

## Performance Tips

### Speed Up Scraping
- Use SSD storage
- Close other applications
- Run on cloud VM with good bandwidth

### Reduce Costs (if using proxies)
- Scrape Trustpilot only (fastest, most reviews)
- Limit max_pages/max_reviews
- Schedule scraping during off-peak hours

## Data Analysis Ideas

Once you have the CSVs:

1. **Pain Point Analysis**: Search for keywords like "slow", "expensive", "support"
2. **Sentiment Trends**: Plot ratings over time
3. **Competitor Comparison**: Compare average ratings and common complaints
4. **Feature Gaps**: Look for "wish" or "need" or "should have"
5. **Switching Triggers**: Search for "switched from", "left", "moved to"

## Legal & Ethical Notes

- ✅ **For research**: Analyzing public reviews for competitive intelligence
- ✅ **Respectful scraping**: Built-in delays, respects rate limits
- ⚠️ **Check ToS**: Review each platform's terms of service
- ❌ **Don't**: Scrape PII, use for spam, violate platform ToS

## Support

For issues or questions:
1. Check the error message
2. Review troubleshooting section above
3. Search for the error online (Playwright has great docs)
4. Modify scraper code as needed (it's well-commented!)

## Next Steps

1. **Run your first scrape** with 2-3 companies to test
2. **Analyze the data** in Excel/Google Sheets
3. **Scale up** to full competitor list
4. **Automate** by scheduling weekly scrapes

---

**Happy scraping! 🚀**

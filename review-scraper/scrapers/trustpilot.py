"""
Trustpilot scraper using direct URLs
"""
import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright
import re


class TrustpilotScraper:
    """Scrapes reviews from Trustpilot using direct URLs"""

    async def scrape_reviews(self, company_name: str, url: str, max_pages: int = 50) -> List[Dict]:
        """Scrape reviews for a company from direct URL"""
        all_reviews = []

        print(f"\n🏢 Scraping {company_name} from Trustpilot...")
        print(f"  🔗 URL: {url}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            page = await context.new_page()

            # Navigate to the URL
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            except Exception as e:
                print(f"  ❌ Failed to load page: {e}")
                await browser.close()
                return []

            page_num = 1

            while page_num <= max_pages:
                print(f"  📄 Scraping page {page_num}...", end="\r")

                # Wait for reviews to load
                try:
                    await page.wait_for_selector('[data-service-review-card-paper]', timeout=10000)
                except:
                    print(f"\n  ⚠️  No reviews found on page {page_num}")
                    break

                await asyncio.sleep(1)

                # Extract reviews on current page
                review_cards = await page.query_selector_all('[data-service-review-card-paper]')

                if not review_cards:
                    print(f"\n  ✅ No more reviews at page {page_num}")
                    break

                for card in review_cards:
                    try:
                        # Rating
                        rating_elem = await card.query_selector('[data-service-review-rating]')
                        rating = None
                        if rating_elem:
                            rating_img = await rating_elem.query_selector('img')
                            if rating_img:
                                alt_text = await rating_img.get_attribute('alt')
                                match = re.search(r'(\d+)', alt_text) if alt_text else None
                                if match:
                                    rating = int(match.group(1))

                        # Title
                        title_elem = await card.query_selector('[data-service-review-title-typography]')
                        title = await title_elem.inner_text() if title_elem else ""

                        # Content
                        content_elem = await card.query_selector('[data-service-review-text-typography]')
                        content = await content_elem.inner_text() if content_elem else ""

                        # Author
                        author_elem = await card.query_selector('[data-consumer-name-typography]')
                        author = await author_elem.inner_text() if author_elem else "Anonymous"

                        # Date
                        date_elem = await card.query_selector('time')
                        date = ""
                        if date_elem:
                            date = await date_elem.get_attribute('datetime')
                            if date:
                                date = date[:10]  # Get YYYY-MM-DD

                        # Verified
                        verified = await card.query_selector('[data-service-review-verify-typography]') is not None

                        all_reviews.append({
                            "company": company_name,
                            "platform": "Trustpilot",
                            "rating": rating,
                            "title": title.strip(),
                            "content": content.strip(),
                            "author": author.strip(),
                            "date": date,
                            "verified": verified,
                            "url": url
                        })

                    except Exception as e:
                        continue

                # Try to go to next page
                try:
                    next_button = await page.query_selector('a[name="pagination-button-next"]')
                    if next_button:
                        # Check if button is disabled
                        is_disabled = await next_button.get_attribute('disabled')
                        aria_disabled = await next_button.get_attribute('aria-disabled')

                        if is_disabled or aria_disabled == 'true':
                            print(f"\n  ✅ Reached last page at page {page_num}")
                            break

                        await next_button.click()
                        await page.wait_for_load_state("networkidle", timeout=10000)
                        page_num += 1
                        await asyncio.sleep(2)
                    else:
                        print(f"\n  ✅ No next button at page {page_num}")
                        break
                except Exception as e:
                    print(f"\n  ⚠️  Pagination error: {e}")
                    break

            await browser.close()

        print(f"  ✅ Total reviews scraped: {len(all_reviews)}")
        return all_reviews


if __name__ == "__main__":
    # Test with a single URL
    async def test():
        scraper = TrustpilotScraper()
        reviews = await scraper.scrape_reviews(
            "Wise",
            "https://uk.trustpilot.com/review/wise.com",
            max_pages=2
        )
        print(f"\n✅ Total reviews: {len(reviews)}")

    asyncio.run(test())

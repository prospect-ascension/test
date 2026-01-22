"""
G2 scraper using direct URLs
"""
import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright
import re


class G2Scraper:
    """Scrapes reviews from G2 using direct URLs"""

    async def scrape_reviews(self, company_name: str, url: str, max_reviews: int = 200) -> List[Dict]:
        """Scrape reviews for a company from direct URL"""
        all_reviews = []

        print(f"\n🏢 Scraping {company_name} from G2...")
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

            print(f"  📄 Loading reviews...")

            # Scroll to load reviews (G2 uses infinite scroll)
            scroll_attempts = 0
            max_scrolls = 20  # Limit scrolling

            while scroll_attempts < max_scrolls:
                # Check current review count
                current_count = len(await page.query_selector_all('[itemprop="review"]'))

                if current_count >= max_reviews:
                    print(f"  ✅ Loaded {current_count} reviews (target reached)")
                    break

                # Scroll down
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)

                # Check if new reviews loaded
                new_count = len(await page.query_selector_all('[itemprop="review"]'))
                if new_count == current_count:
                    print(f"  ✅ No more reviews to load (total: {new_count})")
                    break

                scroll_attempts += 1
                print(f"  📄 Loaded {new_count} reviews...", end="\r")

            # Extract reviews
            print(f"\n  📝 Extracting review data...")
            review_elements = await page.query_selector_all('[itemprop="review"]')

            for idx, review_elem in enumerate(review_elements):
                try:
                    # Rating
                    rating_elem = await review_elem.query_selector('[itemprop="ratingValue"]')
                    rating = await rating_elem.get_attribute('content') if rating_elem else None

                    # Title
                    title_elem = await review_elem.query_selector('[itemprop="name"]')
                    title = await title_elem.inner_text() if title_elem else ""

                    # Content
                    content_elem = await review_elem.query_selector('[itemprop="reviewBody"]')
                    content = await content_elem.inner_text() if content_elem else ""

                    # Author
                    author_elem = await review_elem.query_selector('[itemprop="author"]')
                    author = await author_elem.inner_text() if author_elem else "Anonymous"

                    # Date
                    date_elem = await review_elem.query_selector('time')
                    date = await date_elem.get_attribute('datetime') if date_elem else ""
                    if date:
                        date = date[:10]  # Get YYYY-MM-DD

                    all_reviews.append({
                        "company": company_name,
                        "platform": "G2",
                        "rating": float(rating) if rating else None,
                        "title": title.strip(),
                        "content": content.strip(),
                        "author": author.strip(),
                        "date": date,
                        "verified": True,  # G2 reviews are generally verified
                        "url": url
                    })

                    if (idx + 1) % 10 == 0:
                        print(f"  📝 Extracted {idx + 1} reviews...", end="\r")

                except Exception as e:
                    continue

            await browser.close()

        print(f"\n  ✅ Total reviews scraped: {len(all_reviews)}")
        return all_reviews


if __name__ == "__main__":
    # Test with a single URL
    async def test():
        scraper = G2Scraper()
        reviews = await scraper.scrape_reviews(
            "Wise",
            "https://www.g2.com/products/wise-business/reviews",
            max_reviews=20
        )
        print(f"\n✅ Total reviews: {len(reviews)}")

    asyncio.run(test())

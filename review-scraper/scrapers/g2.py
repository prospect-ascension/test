"""
G2 scraper using Playwright browser automation
"""
import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright, Page
import re


class G2Scraper:
    """Scrapes reviews from G2 using browser automation"""

    BASE_URL = "https://www.g2.com"

    async def search_company(self, page: Page, company_name: str) -> str:
        """Search for a company on G2 and return product URL"""
        print(f"  🔍 Searching for {company_name} on G2...")

        search_url = f"{self.BASE_URL}/search"
        await page.goto(search_url, wait_until="domcontentloaded")

        # Type in search box
        try:
            await page.fill('input[name="query"]', company_name)
            await page.press('input[name="query"]', "Enter")
            await page.wait_for_load_state("networkidle")

            # Look for first product result
            first_result = await page.query_selector('a.product-listing__product-name')
            if first_result:
                href = await first_result.get_attribute('href')
                product_url = f"{self.BASE_URL}{href}"
                print(f"  ✅ Found product: {product_url}")
                return product_url
        except Exception as e:
            print(f"  ⚠️  Search method 1 failed: {e}")

        # Fallback: Try direct URL construction
        slug = company_name.lower().replace(" ", "-").replace(".", "")
        potential_urls = [
            f"{self.BASE_URL}/products/{slug}/reviews",
            f"{self.BASE_URL}/products/{slug}-business/reviews",
            f"{self.BASE_URL}/products/{slug}-for-business/reviews",
        ]

        for url in potential_urls:
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=10000)
                # Check if we're on a valid product page
                title = await page.query_selector('h1')
                if title:
                    print(f"  ✅ Found via direct URL: {url}")
                    return url
            except:
                continue

        print(f"  ❌ Could not find {company_name} on G2")
        return None

    async def scrape_reviews(self, company_name: str, max_reviews: int = 200) -> List[Dict]:
        """Scrape reviews for a company"""
        all_reviews = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            page = await context.new_page()

            # Find company
            product_url = await self.search_company(page, company_name)
            if not product_url:
                await browser.close()
                return []

            # Navigate to reviews page
            reviews_url = product_url if "/reviews" in product_url else f"{product_url}/reviews"
            await page.goto(reviews_url, wait_until="domcontentloaded")

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
                        "url": reviews_url
                    })

                    if (idx + 1) % 10 == 0:
                        print(f"  📝 Extracted {idx + 1} reviews...", end="\r")

                except Exception as e:
                    print(f"\n  ⚠️  Error extracting review {idx}: {e}")
                    continue

            await browser.close()

        print(f"\n  ✅ Total reviews scraped: {len(all_reviews)}")
        return all_reviews


async def scrape_companies(company_names: List[str]) -> List[Dict]:
    """Scrape reviews for multiple companies"""
    scraper = G2Scraper()
    all_reviews = []

    for company_name in company_names:
        print(f"\n🏢 Scraping {company_name} from G2...")
        reviews = await scraper.scrape_reviews(company_name)
        all_reviews.extend(reviews)
        await asyncio.sleep(3)  # Delay between companies

    return all_reviews


if __name__ == "__main__":
    # Test with a single company
    companies = ["Wise"]
    reviews = asyncio.run(scrape_companies(companies))
    print(f"\n✅ Total reviews: {len(reviews)}")

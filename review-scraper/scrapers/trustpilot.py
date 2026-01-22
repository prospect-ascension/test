"""
Trustpilot scraper using Playwright browser automation
"""
import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright, Page
import re


class TrustpilotScraper:
    """Scrapes reviews from Trustpilot using browser automation"""

    BASE_URL = "https://www.trustpilot.com"

    async def search_company(self, page: Page, company_name: str) -> str:
        """Search for a company on Trustpilot and return review URL"""
        print(f"  🔍 Searching for {company_name} on Trustpilot...")

        # Try multiple URL variations
        slug_variations = [
            company_name.lower().replace(" ", "-").replace(".", ""),
            company_name.lower().replace(" ", "").replace(".", ""),
            f"{company_name.lower().replace(' ', '')}.com",
            f"www.{company_name.lower().replace(' ', '')}.com",
            company_name.lower().replace(" ", "-"),
        ]

        for slug in slug_variations:
            url = f"{self.BASE_URL}/review/{slug}"
            try:
                response = await page.goto(url, wait_until="domcontentloaded", timeout=10000)
                if response and response.status == 200:
                    # Check if we're on a valid company page
                    title = await page.query_selector('h1')
                    if title and "Page not found" not in await page.content():
                        print(f"  ✅ Found: {url}")
                        return url
            except:
                continue

        # Fallback: Use search
        try:
            await page.goto(f"{self.BASE_URL}/search", wait_until="domcontentloaded")
            await page.fill('input[name="query"]', company_name)
            await page.press('input[name="query"]', "Enter")
            await page.wait_for_load_state("networkidle", timeout=10000)

            # Click first result
            first_result = await page.query_selector('a[href*="/review/"]')
            if first_result:
                href = await first_result.get_attribute('href')
                url = f"{self.BASE_URL}{href}" if href.startswith('/') else href
                await page.goto(url, wait_until="domcontentloaded")
                print(f"  ✅ Found via search: {url}")
                return url
        except Exception as e:
            print(f"  ⚠️  Search failed: {e}")

        print(f"  ❌ Could not find {company_name} on Trustpilot")
        return None

    async def scrape_reviews(self, company_name: str, max_pages: int = 50) -> List[Dict]:
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
            company_url = await self.search_company(page, company_name)
            if not company_url:
                await browser.close()
                return []

            # Already on the reviews page
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
                            "url": company_url
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

        print(f"\n  ✅ Total reviews scraped: {len(all_reviews)}")
        return all_reviews


async def scrape_companies(company_names: List[str]) -> List[Dict]:
    """Scrape reviews for multiple companies"""
    scraper = TrustpilotScraper()
    all_reviews = []

    for company_name in company_names:
        print(f"\n🏢 Scraping {company_name}...")
        reviews = await scraper.scrape_reviews(company_name)
        all_reviews.extend(reviews)
        await asyncio.sleep(2)  # Delay between companies

    return all_reviews


if __name__ == "__main__":
    # Test with a single company
    companies = ["Wise"]
    reviews = asyncio.run(scrape_companies(companies))
    print(f"\n✅ Total reviews: {len(reviews)}")

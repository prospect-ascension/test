"""
Capterra scraper using Playwright browser automation
"""
import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright, Page
import re


class CapterraScraper:
    """Scrapes reviews from Capterra using browser automation"""

    BASE_URL = "https://www.capterra.com"

    async def search_company(self, page: Page, company_name: str) -> str:
        """Search for a company on Capterra and return product URL"""
        print(f"  🔍 Searching for {company_name} on Capterra...")

        # Try search
        search_url = f"{self.BASE_URL}/search"
        try:
            await page.goto(search_url, wait_until="domcontentloaded")
            await page.fill('input[name="q"]', company_name)
            await page.press('input[name="q"]', "Enter")
            await page.wait_for_load_state("networkidle", timeout=10000)

            # Look for first product result
            first_result = await page.query_selector('a.d-flex.flex-column')
            if first_result:
                href = await first_result.get_attribute('href')
                if href and href.startswith('/p/'):
                    product_url = f"{self.BASE_URL}{href}"
                    print(f"  ✅ Found product: {product_url}")
                    return product_url
        except Exception as e:
            print(f"  ⚠️  Search method failed: {e}")

        # Fallback: Try direct URL construction
        slug = company_name.lower().replace(" ", "-").replace(".", "")
        potential_urls = [
            f"{self.BASE_URL}/software/{slug}",
            f"{self.BASE_URL}/p/{slug}",
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

        print(f"  ❌ Could not find {company_name} on Capterra")
        return None

    async def scrape_reviews(self, company_name: str, max_pages: int = 20) -> List[Dict]:
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

            # Navigate to reviews section
            await page.goto(product_url, wait_until="domcontentloaded")

            # Try to click on "Reviews" tab
            try:
                reviews_tab = await page.query_selector('a[href*="#reviews"], button:has-text("Reviews")')
                if reviews_tab:
                    await reviews_tab.click()
                    await asyncio.sleep(2)
            except:
                pass

            page_num = 1

            while page_num <= max_pages:
                print(f"  📄 Scraping page {page_num}...", end="\r")

                # Wait for reviews to load
                await asyncio.sleep(2)

                # Extract reviews on current page
                review_elements = await page.query_selector_all('[data-test="review-card"], .review-item, [class*="review"]')

                if not review_elements:
                    print(f"\n  ⚠️  No reviews found on page {page_num}")
                    break

                for review_elem in review_elements:
                    try:
                        # Rating (look for stars or numeric rating)
                        rating = None
                        rating_elem = await review_elem.query_selector('[class*="rating"], [class*="stars"]')
                        if rating_elem:
                            rating_text = await rating_elem.inner_text()
                            # Extract number from text like "4.5 out of 5" or "4.5"
                            match = re.search(r'(\d+\.?\d*)', rating_text)
                            if match:
                                rating = float(match.group(1))

                        # Title
                        title_elem = await review_elem.query_selector('h3, h4, [class*="title"]')
                        title = await title_elem.inner_text() if title_elem else ""

                        # Content
                        content_elem = await review_elem.query_selector('[class*="review-text"], [class*="content"], p')
                        content = await content_elem.inner_text() if content_elem else ""

                        # Author
                        author_elem = await review_elem.query_selector('[class*="author"], [class*="reviewer"]')
                        author = await author_elem.inner_text() if author_elem else "Anonymous"

                        # Date
                        date_elem = await review_elem.query_selector('time, [class*="date"]')
                        date = ""
                        if date_elem:
                            date = await date_elem.get_attribute('datetime') or await date_elem.inner_text()
                            if date:
                                date = date[:10] if '-' in date else date

                        # Only add if we have actual content
                        if content.strip():
                            all_reviews.append({
                                "company": company_name,
                                "platform": "Capterra",
                                "rating": rating,
                                "title": title.strip(),
                                "content": content.strip(),
                                "author": author.strip(),
                                "date": date,
                                "verified": True,
                                "url": product_url
                            })

                    except Exception as e:
                        continue

                # Try to find and click "Next" button
                try:
                    next_button = await page.query_selector('a:has-text("Next"), button:has-text("Next"), [class*="next"]')
                    if next_button:
                        is_disabled = await next_button.get_attribute('disabled')
                        if is_disabled:
                            print(f"\n  ✅ Reached last page at page {page_num}")
                            break

                        await next_button.click()
                        await asyncio.sleep(2)
                        page_num += 1
                    else:
                        print(f"\n  ✅ No more pages at page {page_num}")
                        break
                except:
                    print(f"\n  ✅ Could not find next button at page {page_num}")
                    break

            await browser.close()

        # Remove duplicates (sometimes reviews appear on multiple pages)
        unique_reviews = []
        seen_contents = set()
        for review in all_reviews:
            content_hash = review['content'][:100]  # Use first 100 chars as hash
            if content_hash not in seen_contents:
                seen_contents.add(content_hash)
                unique_reviews.append(review)

        print(f"\n  ✅ Total unique reviews scraped: {len(unique_reviews)}")
        return unique_reviews


async def scrape_companies(company_names: List[str]) -> List[Dict]:
    """Scrape reviews for multiple companies"""
    scraper = CapterraScraper()
    all_reviews = []

    for company_name in company_names:
        print(f"\n🏢 Scraping {company_name} from Capterra...")
        reviews = await scraper.scrape_reviews(company_name)
        all_reviews.extend(reviews)
        await asyncio.sleep(3)  # Delay between companies

    return all_reviews


if __name__ == "__main__":
    # Test with a single company
    companies = ["Wise"]
    reviews = asyncio.run(scrape_companies(companies))
    print(f"\n✅ Total reviews: {len(reviews)}")

"""Quick test to verify scrapers work"""
import asyncio
from scrapers.trustpilot import TrustpilotScraper
from scrapers.g2 import G2Scraper
from scrapers.capterra import CapterraScraper


async def test_trustpilot():
    print("\n" + "="*60)
    print("Testing Trustpilot Scraper")
    print("="*60)
    scraper = TrustpilotScraper()
    reviews = await scraper.scrape_reviews("Wise", max_pages=2)
    print(f"✅ Scraped {len(reviews)} reviews from Trustpilot")
    if reviews:
        print(f"Sample review: {reviews[0]['title'][:50]}...")
    return len(reviews) > 0


async def test_g2():
    print("\n" + "="*60)
    print("Testing G2 Scraper")
    print("="*60)
    scraper = G2Scraper()
    reviews = await scraper.scrape_reviews("Wise", max_reviews=20)
    print(f"✅ Scraped {len(reviews)} reviews from G2")
    if reviews:
        print(f"Sample review: {reviews[0]['title'][:50]}...")
    return len(reviews) > 0


async def test_capterra():
    print("\n" + "="*60)
    print("Testing Capterra Scraper")
    print("="*60)
    scraper = CapterraScraper()
    reviews = await scraper.scrape_reviews("Wise", max_pages=1)
    print(f"✅ Scraped {len(reviews)} reviews from Capterra")
    if reviews:
        print(f"Sample review: {reviews[0]['title'][:50]}...")
    return len(reviews) > 0


async def main():
    results = {}

    # Test each scraper
    results['trustpilot'] = await test_trustpilot()
    results['g2'] = await test_g2()
    results['capterra'] = await test_capterra()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for platform, success in results.items():
        status = "✅ WORKING" if success else "❌ NEEDS FIX"
        print(f"{platform.title()}: {status}")

    if all(results.values()):
        print("\n🎉 All scrapers working! Ready to use.")
    else:
        print("\n⚠️  Some scrapers need attention")


if __name__ == "__main__":
    asyncio.run(main())

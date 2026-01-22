#!/usr/bin/env python3
"""
Main CLI tool for scraping reviews from Trustpilot, G2, and Capterra
Uses direct URLs from companies.yaml configuration file
"""
import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime
import yaml
from scrapers.trustpilot import TrustpilotScraper
from scrapers.g2 import G2Scraper
from scrapers.capterra import CapterraScraper


def load_companies():
    """Load company URLs from YAML config"""
    with open('companies.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config['companies']


def save_to_csv(reviews, filename):
    """Save reviews to CSV file"""
    if not reviews:
        print(f"  ⚠️  No reviews to save for {filename}")
        return

    df = pd.DataFrame(reviews)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"  ✅ Saved {len(reviews)} reviews to {filepath}")


async def scrape_all_platforms(companies):
    """Scrape all platforms for given companies"""
    all_reviews = []

    trustpilot_scraper = TrustpilotScraper()
    g2_scraper = G2Scraper()
    capterra_scraper = CapterraScraper()

    print("\n" + "="*60)
    print("🚀 TRUSTPILOT SCRAPING")
    print("="*60)
    trustpilot_reviews = []
    for company in companies:
        if company.get('trustpilot'):
            reviews = await trustpilot_scraper.scrape_reviews(
                company['name'],
                company['trustpilot']
            )
            trustpilot_reviews.extend(reviews)
            await asyncio.sleep(3)  # Delay between companies
        else:
            print(f"\n⏭️  Skipping {company['name']} (no Trustpilot URL)")

    all_reviews.extend(trustpilot_reviews)
    save_to_csv(trustpilot_reviews, "trustpilot_reviews.csv")

    print("\n" + "="*60)
    print("🚀 G2 SCRAPING")
    print("="*60)
    g2_reviews = []
    for company in companies:
        if company.get('g2'):
            reviews = await g2_scraper.scrape_reviews(
                company['name'],
                company['g2']
            )
            g2_reviews.extend(reviews)
            await asyncio.sleep(3)  # Delay between companies
        else:
            print(f"\n⏭️  Skipping {company['name']} (no G2 URL)")

    all_reviews.extend(g2_reviews)
    save_to_csv(g2_reviews, "g2_reviews.csv")

    print("\n" + "="*60)
    print("🚀 CAPTERRA SCRAPING")
    print("="*60)
    capterra_reviews = []
    for company in companies:
        if company.get('capterra'):
            reviews = await capterra_scraper.scrape_reviews(
                company['name'],
                company['capterra']
            )
            capterra_reviews.extend(reviews)
            await asyncio.sleep(3)  # Delay between companies
        else:
            print(f"\n⏭️  Skipping {company['name']} (no Capterra URL)")

    all_reviews.extend(capterra_reviews)
    save_to_csv(capterra_reviews, "capterra_reviews.csv")

    # Save combined results
    print("\n" + "="*60)
    print("💾 SAVING COMBINED RESULTS")
    print("="*60)
    save_to_csv(all_reviews, "all_reviews.csv")

    # Print summary
    print("\n" + "="*60)
    print("📊 SCRAPING SUMMARY")
    print("="*60)
    print(f"Total companies scraped: {len(companies)}")
    print(f"Total reviews collected: {len(all_reviews)}")
    print(f"\nBreakdown by platform:")
    print(f"  - Trustpilot: {len(trustpilot_reviews)} reviews")
    print(f"  - G2: {len(g2_reviews)} reviews")
    print(f"  - Capterra: {len(capterra_reviews)} reviews")
    print("\nBreakdown by company:")

    if all_reviews:
        df = pd.DataFrame(all_reviews)
        company_counts = df.groupby('company').size().to_dict()
        for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {company}: {count} reviews")

    print("\n✅ All files saved to ./output/ directory")
    print("="*60)


def main():
    """Main entry point"""
    print("="*60)
    print("🔍 REVIEW SCRAPER - Trustpilot, G2, Capterra")
    print("="*60)

    # Load companies from YAML
    try:
        companies = load_companies()
        print(f"\n✅ Loaded {len(companies)} companies from companies.yaml")
        print("\n📋 Companies to scrape:")
        for i, company in enumerate(companies, 1):
            platforms = []
            if company.get('trustpilot'): platforms.append('Trustpilot')
            if company.get('g2'): platforms.append('G2')
            if company.get('capterra'): platforms.append('Capterra')
            print(f"   {i}. {company['name']} ({', '.join(platforms)})")
    except Exception as e:
        print(f"\n❌ Error loading companies.yaml: {e}")
        print("Make sure companies.yaml exists in the current directory.")
        return

    print("\n⏱️  This may take 30-60 minutes depending on review volume...")
    print("    (Press Ctrl+C to cancel)\n")

    try:
        asyncio.run(scrape_all_platforms(companies))
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

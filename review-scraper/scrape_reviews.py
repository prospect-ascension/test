#!/usr/bin/env python3
"""
Main CLI tool for scraping reviews from Trustpilot, G2, and Capterra
"""
import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime
from scrapers.trustpilot import scrape_companies as scrape_trustpilot
from scrapers.g2 import scrape_companies as scrape_g2
from scrapers.capterra import scrape_companies as scrape_capterra


def save_to_csv(reviews, filename):
    """Save reviews to CSV file"""
    if not reviews:
        print(f"  ⚠️  No reviews to save for {filename}")
        return

    df = pd.DataFrame(reviews)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename
    df.to_csv(filepath, index=False)
    print(f"  ✅ Saved {len(reviews)} reviews to {filepath}")


async def scrape_all_platforms(company_names):
    """Scrape all platforms for given companies"""
    all_reviews = []

    print("\n" + "="*60)
    print("🚀 TRUSTPILOT SCRAPING")
    print("="*60)
    trustpilot_reviews = await scrape_trustpilot(company_names)
    all_reviews.extend(trustpilot_reviews)
    save_to_csv(trustpilot_reviews, "trustpilot_reviews.csv")

    print("\n" + "="*60)
    print("🚀 G2 SCRAPING")
    print("="*60)
    g2_reviews = await scrape_g2(company_names)
    all_reviews.extend(g2_reviews)
    save_to_csv(g2_reviews, "g2_reviews.csv")

    print("\n" + "="*60)
    print("🚀 CAPTERRA SCRAPING")
    print("="*60)
    capterra_reviews = await scrape_capterra(company_names)
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
    print(f"Total companies scraped: {len(company_names)}")
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

    # Get company names from user
    print("\n📝 Enter company names to scrape (comma-separated):")
    print("   Example: Wise, Revolut Business, Airwallex")
    print()

    user_input = input("Companies: ").strip()

    if not user_input:
        print("❌ No companies provided. Using default list...")
        companies = [
            "Wise",
            "Revolut Business",
            "Airwallex",
            "WorldFirst",
            "Payoneer",
            "Aspire",
            "Statrys",
            "OFX",
            "Currencycloud"
        ]
    else:
        companies = [c.strip() for c in user_input.split(",") if c.strip()]

    print(f"\n🎯 Will scrape reviews for {len(companies)} companies:")
    for i, company in enumerate(companies, 1):
        print(f"   {i}. {company}")

    print("\n⏱️  This may take 10-30 minutes depending on review volume...")
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

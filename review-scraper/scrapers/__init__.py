"""Scrapers package"""
from .trustpilot import TrustpilotScraper
from .g2 import G2Scraper
from .capterra import CapterraScraper

__all__ = ['TrustpilotScraper', 'G2Scraper', 'CapterraScraper']

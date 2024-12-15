# Scrape new sales listing Dec 14, 2024
import asyncio
from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
import arrow # for handling datetime: pip install arrow
from datetime import datetime
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()
SCRAPFLY = ScrapflyClient(key=os.getenv('SCRAPFLY_API_KEY'))

async def scrape_feed(url) -> Dict[str, datetime]:
    """scrape Redfin sitemap and return url:datetime dictionary"""
    result = await SCRAPFLY.async_scrape(ScrapeConfig(url, asp=True, country="US"))
    selector = result.selector
    results = {}
    for item in selector.xpath("//url"):
        url = item.xpath(".//loc/text()").get()
        pub_date = item.xpath(".//lastmod/text()").get()
        results[url] = arrow.get(pub_date).datetime
    return results


async def run():
    data = await scrape_feed("https://www.redfin.com/newest_listings.xml")
    print(data.keys())

if __name__ == "__main__":
    asyncio.run(run())


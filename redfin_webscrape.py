import asyncio
import json
from typing import List, Dict
from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
import arrow # for handling datetime: pip install arrow
from datetime import datetime
from typing import Dict
from fpdf import FPDF
import os
from dotenv import load_dotenv

load_dotenv()
SCRAPFLY = ScrapflyClient(key=os.getenv('SCRAPFLY_API_KEY'))

def parse_property_for_rent(response: ScrapeApiResponse):
    """get the rental ID from the HTML to use it in the API"""
    selector = response.selector
    data = selector.xpath("//meta[@property='og:image']").attrib["content"]
    try:
        rental_id = data.split("rent/")[1].split("/")[0]
        # validate the rentalId
        assert len(rental_id) == 36
        return rental_id
    except:
        print("proeprty isn't for rent")
        return None


async def scrape_property_for_rent(urls: List[str]) -> list[Dict]:
    """scrape properties for rent from the API"""
    api_urls = []
    properties = []
    for url in urls:
        response_html = await SCRAPFLY.async_scrape(ScrapeConfig(url, asp=True, country="US"))
        rental_id = parse_property_for_rent(response_html)
        if rental_id:
            api_urls.append(
                f"https://www.redfin.com/stingray/api/v1/rentals/{rental_id}/floorPlans"
            )
    # add the property pages API URLs to a scraping list
    to_scrape = [ScrapeConfig(url, country="US") for url in api_urls]
    async for response in SCRAPFLY.concurrent_scrape(to_scrape):
        properties.append(json.loads(response.content))
    print(f"scraped {len(properties)} property listings for rent")
    return properties

def parse_property_for_sale(response: ScrapeApiResponse) -> List[Dict]:
    """parse property data from the HTML"""
    selector = response.selector
    price = selector.xpath("//div[@data-rf-test-id='abp-price']/div/text()").get()
    estimated_monthly_price = "".join(selector.xpath("//span[@class='est-monthly-payment']/text()").getall())
    address = (
        "".join(selector.xpath("//div[contains(@class, 'street-address')]/text()").getall())
        + " " + "".join(selector.xpath("//div[contains(@class, 'cityStateZip')]/text()").getall())
    )
    description = selector.xpath("//div[@id='marketing-remarks-scroll']/p/span/text()").get()
    images = [
        image.attrib["src"]
        #for image in selector.xpath("//img[contains(@class, 'widenPhoto')]")
        for image in selector.xpath("//img[contains(@class, ' landscape')]")
    ]
    details = [
        "".join(text_content.getall())
        for text_content in selector.css("div .keyDetails-value::text")
    ]

    features_data = {}
    for feature_block in selector.css(".amenity-group ul div.title"):
        label = feature_block.css("::text").get()
        features = feature_block.xpath("following-sibling::li/span")
        features_data[label] = [
            "".join(feat.xpath(".//text()").getall()).strip() for feat in features
        ]
    return {
        "address": address,
        "description": description,
        "price": price,
        "estimatedMonthlyPrice": estimated_monthly_price,
        "propertyUrl": str(response.context["url"]),
        "attachments": images,
        "details": details,
        "features": features_data,
    }


async def scrape_property_for_sale(urls: List[str]) -> List[Dict]:
    """scrape properties for sale data from HTML"""
    # add the property pages to a scraping list
    to_scrape = [ScrapeConfig(url, asp=True, country="US") for url in urls]
    properties = []
    # scrape all property pages concurrently
    async for response in SCRAPFLY.concurrent_scrape(to_scrape):
        data = parse_property_for_sale(response)
        properties.append(data)
    print(f"scraped {len(properties)} property listings for sale")
    return properties


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


f = open("/Users/weicongsu/PycharmProjects/home_search_agent_rag/data/house/opening_dec_14_2024.txt", "r") # change to your local directory
urls = f.read()
urls = urls.split(", ")
opening_list = []
for url in urls[0:100]:
    url = url.replace("{","")
    url = url.replace("\'","")
    url = url.replace("}", "")
    opening_list.append(url)

async def run():
    for index, opening in enumerate(opening_list[0:100]):
        try:
            print([opening])
            data = await scrape_property_for_sale([opening])
            # save FPDF() class into a
            # variable pdf
            pdf = FPDF()
            # Add a page
            pdf.add_page()
            # set style and size of font
            # that you want in the pdf
            pdf.set_font("Arial", size=15)
            description = data[0]['description']
            sentences = description.split(". ")
            pdf.write(8, 'Property_URL:\n' + "\'" + data[0]['propertyUrl'] + '\'' + ". \n")
            for sentence in sentences:
                sentence = sentence.strip()  # Remove leading/trailing whitespaces
                if sentence:
                    pdf.write(8, sentence + ". \n")  # Add newline after each sentence

            pdf.output("/Users/weicongsu/PycharmProjects/home_search_agent_rag/data/house/" +\
                str(index) + ".pdf") # change to your local directory
        except: pass

if __name__ == "__main__":
     asyncio.run(run())








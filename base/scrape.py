import requests, argparse, transaction
from ZODB import DB, FileStorage
from bs4 import BeautifulSoup

HEADERS = ({
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
})


class Scraper(object):
    def __init__(self, db=None):
        self.HEADERS = HEADERS
        self.webpage_text = None
        self.webpage_soup = None
        self.db = DB(db) # DB is in memory if None

        # Default parser, gets url from cmdline arg
        self.parser = argparse.ArgumentParser(description="Scraper Args.")
        self.parser.add_argument("--url", required=False, action="store", type=str, help="URL to scrape")
        args = self.parser.parse_args()

        # If a URL was passed via cmdline, use it here
        self.URL = args.url


    def get_html_data(self, URL=None):
        if URL is None:
            # Use optional URL argument if it was passed, otherwise use the scrapers default URL (from arg)
            URL = self.URL
        page = requests.get(URL, headers=self.HEADERS)
        self.webpage_text = page.text
        self.webpage_soup = BeautifulSoup(page.content, "lxml")

import os
import re
import tempfile
import time
import unicodedata

import requests
from bs4 import BeautifulSoup
from logger import get_logger
from pydantic import BaseModel

logger = get_logger(__name__)

class CrawlWebsite(BaseModel):
    url : str
    js : bool = False
    depth : int = 1
    max_pages : int = 100
    max_time : int = 60
    bypass_max_time: bool = False
    bypass_max_pages: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        self.visited = set()
        self.page_counter = 0
        self.start_time = time.perf_counter()

    def _crawl(self, url, depth):
        if url in self.visited or depth == 0 or (not self.bypass_max_pages and self.page_counter >= self.max_pages) or (not self.bypass_max_time and (time.perf_counter() - self.start_time) > self.max_time):
            return
        try:
            logger.info(f"Trying to get url: {url}")
            response = requests.get(url)
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        except requests.exceptions.RequestException as e:
            logger.error(f'Error occurred when trying to get {url}: {e}')
            return

        self.visited.add(url)
        self.page_counter += 1
        logger.info(f"Visited URL: {url}")
        content = response.text

        file_name = slugify(url) + ".html"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(content)
        logger.info(f"Saved HTML content of {url} to file: {file_name}")
        
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a', href=True):
            if link['href'].startswith('http') and not link['href'].startswith('#'):
                self._crawl(link['href'], depth - 1)

    def process(self):
        logger.info(f"Starting to process URL: {self.url}")
        self._crawl(self.url, self.depth)
        logger.info("Process complete.")

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text

logger.info("Starting crawl process")
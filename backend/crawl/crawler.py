import os
import re
import tempfile
import time
import unicodedata

import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import GitLoader
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

    def process(self):
        content = self._crawl(self.url)

        # Create a file
        file_name = slugify(self.url) + ".html"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(content)
            # Process the file

        if content:
            return temp_file_path, file_name
        else:
            return None

    def checkGithub(self):
        if "github.com" in self.url:
            return True
        else:
            return False


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text

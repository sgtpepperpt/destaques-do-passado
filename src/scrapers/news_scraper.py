from collections import defaultdict
from enum import Enum

from bs4 import BeautifulSoup


class Importance(str, Enum):
    FEATURE: str = 5
    LARGE: str = 4
    SMALL: str = 3
    LATEST: str = 2
    RELATED: str = 1
    UNKNOWN: str = 0


class ScraperCentral:
    __scrapers = defaultdict(list)

    def register_scraper(self, scraper):
        s = scraper()
        self.__scrapers[s.source].append(scraper())
        self.__scrapers[s.source].sort()

    def scrape_page(self, source, date, page_content):
        for scraper in self.__scrapers[source]:
            if scraper.is_admissible(date):
                soup = BeautifulSoup(page_content, 'html.parser')
                return scraper.scrape_page(soup)

        raise Exception('Scraper not defined!')


class NewsScraper:
    def is_admissible(self, date):
        if not self.cutoff:
            raise Exception('Cutoff undefined!')

        return int(date) <= self.cutoff

    def __lt__(self, other):
        if not self.cutoff or not other.cutoff:
            raise Exception('Cutoff undefined!')

        return self.cutoff < other.cutoff

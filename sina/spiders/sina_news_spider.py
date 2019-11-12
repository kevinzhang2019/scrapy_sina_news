import scrapy
from bs4 import BeautifulSoup
import re


class sina(scrapy.Spider):
    name = "sina"
    start_urls = ['https://news.sina.com.cn/']
    custom_settings = {
        "LOG_LEVEL": "ERROR"
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        tags = soup.findAll("a", href=re.compile(r"sina.*\d{4}-\d{2}-\d{2}.*shtml$"))
        for tag in tags:
            url = tag.get("href")
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        try:
            soup = BeautifulSoup(response.body, "lxml")
            title = self.extract_title(soup)
            print(f"{title} {response.url}")
            if title is None:
                raise Exception(f"title not found {response.url}")
        except Exception as e:
            self.logger.error(str(e))

    @staticmethod
    def extract_title(soup):
        selectors = ["h1.main-title", "h1#main-title", "h1#artibodyTitle", "h1.l_tit", "span.location h1"]
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                title = soup.select(selector)[0].text
                return title

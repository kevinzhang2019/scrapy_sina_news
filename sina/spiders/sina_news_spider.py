import scrapy
from bs4 import BeautifulSoup
import re


class sina(scrapy.Spider):
    name = "sina"
    start_urls = ['https://news.sina.com.cn/']

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        tags = soup.findAll("a", href=re.compile(r"sina.*\d{4}-\d{2}-\d{2}.*shtml$"))
        for tag in tags:
            print(f"{tag.text.strip()} {tag.get('href')}")

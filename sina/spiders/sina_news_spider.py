import scrapy
from bs4 import BeautifulSoup
import re
from datetime import datetime
import traceback


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
            # title = self.extract_title(soup)
            # print(f"{title} {response.url}")
            # if title is None:
            #     raise Exception(f"title not found {response.url}")

            public_date = self.extract_date(soup, response.url)
            print(f"{public_date}")
            if public_date is None:
                raise Exception(f"datetime not found {response.url}")

        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(traceback.format_exc())

    @staticmethod
    def extract_title(soup):
        selectors = ['h1.main-title', 'h1.l_tit', '#artibodyTitle',
                     'h1#main_title', 'h1.title', 'div.catuncle-title h1',
                     'div.article-header h1', 'div.titleArea h1',
                     'span.location h1', 'h4.title', 'div.crticalcontent h1 span',
                     'div.news_text h1', 'h1.art_tit_h1', 'div.conleft_h1 h1',
                     'h1.m-atc-title', 'div.b_txt h1 a']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                title = soup.select(selector)[0].text
                return title

    @staticmethod
    def extract_date(soup, url):
        selectors = ["span.date", "span.titer", "span#pub_date", "span.time-source", "div.l_infoBox span",
                     "span#pub_date", "p.source-time span"]
        date = None
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                date = soup.select(selector)[0].text

        # patterns = [
        #     r"\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}",
        #     r"\d{4}年\d{2}月\d{2}日\d{2}:\d{2}",
        #     r"\d{4}-\d{2}-\d{2}",
        #     r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
        # ]
        date_patterns = [r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2}) (?P<h>\d{2}):(?P<M>\d{2})",
                         r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2}) (?P<h>\d{2}):(?P<M>\d{2})",
                         r"(?P<y>\d{4})年(?P<m>\d{2})月(?P<d>\d{2})日 (?P<h>\d{2}):(?P<M>\d{2})",
                         r"(?P<y>\d{4})年(?P<m>\d{2})月(?P<d>\d{2})日(?P<h>\d{2}):(?P<M>\d{2})"]
        if date is not None:
            for pattern in date_patterns:
                if len(re.findall(pattern, date)) > 0:
                    match = re.findall(pattern, date)[0]
                    date = datetime(int(match[0]), int(match[1]), int(match[2]), int(match[3]), int(match[4]))
                    return date
        match = re.findall(r"\d{4}-\d{2}-\d{2}", url)[0]
        return datetime(int(match[0]), int(match[1]), int(match[2]))

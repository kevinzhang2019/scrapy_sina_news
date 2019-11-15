import scrapy
from bs4 import BeautifulSoup
import re
from datetime import datetime
import traceback
from sina.items import SinaItem


class sina(scrapy.Spider):
    name = "sina"
    start_urls = ['https://news.sina.com.cn/']
    custom_settings = {
        "LOG_LEVEL": "ERROR"
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        tags = soup.find_all('a', href=re.compile('(?=^http.*sina.*\d{4}-\d{2}-\d{2}.*html$)'  # doc pattern
                                                  '(?=^((?!video).)*$)'  # ignore video
                                                  '(?=^((?!photo).)*$)'  # ignore photo
                                                  '(?=^((?!slide).)*$)'  # ignore photo
                                                  '(?=^((?!csj\/author).)*$)'  # ignore csj/s=author
                                                  ))
        for tag in tags:
            url = tag.get("href")
            yield scrapy.Request(url, callback=self.parse_detail_and_continue_crawling)

    def parse_detail_and_continue_crawling(self, response):
        try:
            soup = BeautifulSoup(response.body, "lxml")
            title = self.extract_title(soup)
            if title is None:
                raise Exception(f"title not found {response.url}")

            public_date = self.extract_date(soup, response.url)
            if public_date is None:
                raise Exception(f"datetime not found {response.url}")

            keywords = self.extract_keyword(soup)
            if keywords is None:
                keywords = ""
                self.logger.warning("Keyword can't find")

            content = self.extract_content(soup)
            if content is None:
                raise Exception(f"Content can found {response.url}")

            source = self.extract_source(soup)
            if source is None:
                raise Exception(f"Source can found {response.url}")

            item = SinaItem(title=title, keywords=keywords, source=source, content=content, public_date=public_date,
                            url=response.url)
            yield item
            print(f"{title} {public_date} {keywords} {source} {content}")
        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(traceback.format_exc())

        # continue crawling
        tags = soup.find_all('a', href=re.compile('(?=^http.*sina.*\d{4}-\d{2}-\d{2}.*html$)'  # doc pattern
                                                  '(?=^((?!video).)*$)'  # ignore video
                                                  '(?=^((?!photo).)*$)'  # ignore photo
                                                  '(?=^((?!slide).)*$)'  # ignore photo
                                                  '(?=^((?!csj\/author).)*$)'  # ignore csj/s=author
                                                  ))
        for tag in tags:
            url = tag.get("href")
            yield scrapy.Request(url, callback=self.parse_detail_and_continue_crawling)

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

    @staticmethod
    def extract_keyword(soup):
        selectors = [
            "div.keywords a", "p.art_keywords a", "span.source ent-source", "div#keywords a",
            "div.date-source a", "div.l_articleTip clearfix a", "span.source", "div.content_label_list a",
            "div.content_label_list a"
        ]
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                keywords = soup.select(selector)
                return ",".join([keyword.text.strip() for keyword in keywords])

    @staticmethod
    def extract_content(soup):
        selectors = ['div.article p', 'div#artibody p', 'div.mainContent p',
                     'div.article-body p', 'div#editHTML p', 'div.article-content p',
                     'div.l_articleBody p', 'div.catuncle-p p',
                     'div#artibody div p', 'div#articleContent p',
                     'div#fonttext p', 'div.pingcetext p',
                     'div.s_infor p', 'div.fonttext p']
        for selector in selectors:
            if len(soup.select(selector)) > 0:
                content = soup.select(selector)
                return "\n".join([artical.text.strip() for artical in content])[:10]

    @staticmethod
    def extract_source(soup):
        selectors = ['span.source', 'a.source', 'span#art_source',
                     'span#media_name a', 'p.origin span.linkRed02',
                     'span#media_name', 'span.time-source span a', 'a.ent-source',
                     'div.l_infoBox em', 'div.article_tit', 'span.time-source a',
                     'span#author_ename a', 'div#m_atc_original p',
                     'div.b_txt p', 'p.art_p']
        for selector in selectors:
            if len(soup.select(selector)) > 0:
                source = soup.select(selector)[0]
                return source.text.strip()

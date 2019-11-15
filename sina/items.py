# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    title = scrapy.Field()
    keywords = scrapy.Field()
    public_date = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()

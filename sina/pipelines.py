# -*- coding: utf-8 -*-
import pymysql


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaPipeline(object):

    def __init__(self):
        self.connect = pymysql.Connect(host="127.0.0.1", user="root", port=3306, database="news", charset="utf8",
                                       passwd='root')
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        sql = "insert into sina(title,keywords,public_date,content,source,url)values(%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (
            item['title'], item['keywords'], item['public_date'], item['content'], item['source'], item['url']))
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

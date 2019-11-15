# -*- coding: utf-8 -*-
import pymysql


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaPipeline(object):

    def __init__(self):
        self.connect = pymysql.Connect(host="127.0.0.1",user="root", port=3306, database="bigdata", charset="utf8",
                                       )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        sql = f"insert into sina(title,keywords,public_date,content,source,url) values(" \
              f"{item.title},{item.keywords},{item.public_date},{item.content},{item.source},{item.url})"
        self.cursor.execute(sql)
        self.connect.commit()
        return item

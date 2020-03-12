# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .database.mongodb_con import Mongo_Database


class ShuqugeSpiderPipeline(object):
    def process_item(self, item, spider):
        mongo_c = Mongo_Database()
        mongo_c.insert_data(item)
        return item



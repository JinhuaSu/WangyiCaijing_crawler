# -*- coding: utf-8 -*-

import pymongo
import pandas as pd
import os
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlDataPipeline(object):
    def process_item(self, item, spider):
        return item

class PolicyMongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.mongo_col = spider.name
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.mongo_col].drop()

    def close_spider(self, spider):
        if not os.path.exists('../../data/excel/%s' % spider.name):
            os.makedirs('../../data/excel/%s' % spider.name)
        table = self.db[self.mongo_col]
        data_list = []
        for raw_dict in table.find():
            #data_list.append({key:value for key,value in  raw_dict.items() if key in ['UID','title','date','url']})
            data_list.append({key:raw_dict[key] for key in ['UID','title','date','url']})
        df = pd.DataFrame(data_list)
        print(df)
        df.to_excel('../../data/excel/%s/news_list.xls' % spider.name)
        self.client.close()

    def process_item(self, item, spider):
        table = self.db[self.mongo_col]
        if item['crawl state'] == 'half':
            table.insert(item)
        else:
            table.update_one({'UID':item['UID']},{'$set':item},upsert=True)
        return item
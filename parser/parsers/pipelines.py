# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import csv

class ParsersPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.name + '.csv', 'w', encoding='utf8')
        self.fields = ["date", "url", "edition", "topics", "authors", "title", "summary", "text"]
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        self.file.write(','.join(self.fields) + '\n')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        dt = datetime.datetime.strptime(item["date"][0], spider.config.date_format)
        item["title"] = spider.process_title(item["title"][0])
        item["summary"] = spider.process_summary(item["summary"][0]) if "summary" in item else "-"
        item["topics"] = item["topics"][0] if "topics" in item else "-"
        item["authors"] = ','.join(item.get("authors", [""]))
        item["edition"] = item["edition"][0]
        item["url"] = item["url"][0]
        item["text"] = spider.process_text(item["text"])
        item["date"] = dt.strftime("%Y-%m-%d %H:%M:%S")

        if dt.date() < spider.until_date:
            return item
        line = (item["date"], item["url"], item["edition"], item["topics"],
                item["authors"], item["title"], item["summary"], item["text"])
        self.writer.writerow(line)
        return item

# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import json

class ParsersPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.name + '.jsonl', 'w', encoding='utf8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        dt = datetime.datetime.strptime(item["date"][0], spider.config.date_format)
        item["title"] = spider.process_title(item["title"][0])
        item["summary"] = spider.process_summary(item["summary"][0]) if "summary" in item else None
        item["topics"] = item["topics"][0] if "topics" in item else None
        item["authors"] = [a.strip() for a in item.get("authors", []) if len(a) > 2]
        item["edition"] = None if item["edition"][0] == '-' else item["edition"][0]
        item["url"] = item["url"][0]
        item["text"] = spider.process_text(item["text"])
        item["date"] = dt.strftime("%Y-%m-%d %H:%M:%S")

        if dt.date() < spider.until_date:
            return item
        record = {
            "date": item["date"],
            "url": item["url"],
            "edition": item["edition"],
            "topics": item["topics"],
            "authors": item["authors"],
            "title": item["title"],
            "summary": item["summary"],
            "text": item["text"]
        }
        self.file.write(json.dumps(record, ensure_ascii=False).strip() + "\n")
        return item

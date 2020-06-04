# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Document(scrapy.Item):
    title = scrapy.Field()
    summary = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    edition = scrapy.Field()
    topics = scrapy.Field()
    authors = scrapy.Field()

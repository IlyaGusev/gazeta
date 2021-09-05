# -*- coding: utf-8 -*-

# Scrapy settings for parsers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'parsers'

SPIDER_MODULES = ['parsers.spiders']
NEWSPIDER_MODULE = 'parsers.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'gazeta (+github.com/IlyaGusev/gazeta)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'parsers.pipelines.ParsersPipeline': 300,
}

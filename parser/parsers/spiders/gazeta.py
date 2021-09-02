# From https://github.com/ods-ai-ml4sg/proj_news_viz/blob/master/scraping/newsbot/newsbot/spiders/gazeta.py
# Main contributor: https://github.com/Teoretic6

from datetime import datetime

from scrapy import Request, Selector

from parsers.spiders.base import NewsSpider, NewsSpiderConfig

class GazetaSpider(NewsSpider):
    name = "gazeta"
    base_url = "https://www.gazeta.ru/news/?p=page&d={}"
    start_urls = [base_url.format(int(datetime.utcnow().timestamp()))]

    config = NewsSpiderConfig(
        title_path="//div[contains(@itemprop, 'alternativeHeadline')]//text() | //h1/text()",
        date_path="//time[contains(@itemprop, 'datePublished')]/@datetime",
        date_format="%Y-%m-%dT%H:%M:%S%z",
        text_path="//div[contains(@itemprop, 'articleBody')]//p//text()",
        summary_path="//span[contains(@itemprop, 'description')]//text()",
        topics_path="//div[contains(@class, 'active')]/a/span/text()",
        authors_path="//span[contains(@itemprop, 'author')]//text()",
    )

    def parse(self, response):
        links = response.xpath("//div[contains(@class, 'b_ear-title')]/a/@href").extract()
        dates = response.xpath("//div[contains(@class, 'b_ear')]/@data-pubtime").extract()
        assert len(links) == len(dates), "{} {}".format(len(links), len(dates))
        min_pub_time = None
        until_pub_time = int(datetime.combine(self.until_date, datetime.min.time()).timestamp())
        for url, pub_time in zip(links, dates):
            pub_time = int(pub_time)
            min_pub_time = pub_time if not min_pub_time else min(min_pub_time, pub_time)
            if min_pub_time <= until_pub_time:
                break
            url = "https://www.gazeta.ru" + url
            if url.endswith('.shtml') and not url.endswith('index.shtml'):
                yield Request(url=url, callback=self.parse_document)
        if min_pub_time and min_pub_time > until_pub_time:
            yield Request(url=self.base_url.format(min_pub_time), callback=self.parse)


    def parse_document(self, response):
        for res in super().parse_document(response):
            # Remove advertisement blocks
            ad_parts = ('\nРеклама\n', '\n.AdCentre_new_adv', ' AdfProxy.ssp', '\nset_resizeblock_handler')
            if "text" not in res:
                return
            res['text'] = [x for x in res['text'] if x != '\n' and not x.startswith(ad_parts)]
            res["text"] = [x.replace("\xa0", " ") for x in res['text']]

            # Remove ":" in timezone
            pub_dt = res['date'][0]
            res['date'] = [pub_dt[:-3] + pub_dt[-3:].replace(':', '')]

            yield res

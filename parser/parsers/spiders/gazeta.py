# From https://github.com/ods-ai-ml4sg/proj_news_viz/blob/master/scraping/newsbot/newsbot/spiders/gazeta.py
# Main contributor: https://github.com/Teoretic6

from datetime import datetime

from scrapy import Request, Selector

from parsers.spiders.base import NewsSpider, NewsSpiderConfig

class GazetaSpider(NewsSpider):
    name = "gazeta"
    start_urls = ["https://www.gazeta.ru/sitemap.xml"]

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
        body = response.body
        links = Selector(text=body).xpath('//loc/text()').getall()
        last_modif_dts = Selector(text=body).xpath('//lastmod/text()').getall()
        for link, last_modif_dt in zip(links, last_modif_dts):
            last_modif_dt = datetime.strptime(last_modif_dt.replace(':', ''), '%Y-%m-%dT%H%M%S%z')
            if last_modif_dt.date() >= self.until_date:
                yield Request(url=link, callback=self.parse_sub_sitemap)

    def parse_sub_sitemap(self, response):
        body = response.body
        links = Selector(text=body).xpath('//loc/text()').getall()
        last_modif_dts = Selector(text=body).xpath('//lastmod/text()').getall()

        for link, last_modif_dt in zip(links, last_modif_dts):
            last_modif_dt = datetime.strptime(last_modif_dt.replace(':', ''), '%Y-%m-%dT%H%M%S%z')
            if last_modif_dt.date() >= self.until_date:
                yield Request(url=link, callback=self.parse_articles_sitemap)

    def parse_articles_sitemap(self, response):
        # Parse sub sitemaps
        body = response.body
        links = Selector(text=body).xpath('//loc/text()').getall()
        last_modif_dts = Selector(text=body).xpath('//lastmod/text()').getall()

        for link, last_modif_dt in zip(links, last_modif_dts):
            # Convert last_modif_dt to datetime
            last_modif_dt = datetime.strptime(last_modif_dt.replace(':', ''), '%Y-%m-%dT%H%M%S%z')

            if last_modif_dt.date() >= self.until_date:
                if link.endswith('.shtml') and not link.endswith('index.shtml'):
                    yield Request(url=link, callback=self.parse_document)

    def parse_document(self, response):
        for res in super().parse_document(response):
            # Remove advertisement blocks
            ad_parts = ('\nРеклама\n', '\n.AdCentre_new_adv', ' AdfProxy.ssp', '\nset_resizeblock_handler')
            if "text" not in res:
                return
            res['text'] = [x for x in res['text'] if x != '\n' and not x.startswith(ad_parts)]

            # Remove ":" in timezone
            pub_dt = res['date'][0]
            res['date'] = [pub_dt[:-3] + pub_dt[-3:].replace(':', '')]

            yield res

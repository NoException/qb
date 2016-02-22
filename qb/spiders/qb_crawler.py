# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from qb.items import QbItem
from scrapy.spiders.crawl import CrawlSpider


class QbCrawlerSpider(CrawlSpider):
    name = "qb_crawler"
    allowed_domains = ["qiushibaike.com"]
    start_urls = ["http://www.qiushibaike.com/textnew/"]

#     rules = [Rule(LinkExtractor(allow=r'/textnew/page/[0-9]/?s=*'), callback='parse_item', follow=True)]

    def parse_item(self, response):
        questions = Selector(response).xpath('//div[@class="article block untagged mb15"]')
        for question in questions:
            item = QbItem()
            item['author'] = question.xpath('div[@class="author clearfix"]/a[@title=*]/h2/text()').extract()[0]
            item['content'] = question.xpath('div[@class="content"]/text()').extract()[0]
            yield item

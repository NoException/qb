
from scrapy import Spider
from scrapy.selector import Selector
from qb.items import QbItem
import scrapy

# def debug(msg):  
#         scrapy.log.msg(msg.decode("utf-8").encode("gb2312"), level=scrapy.log.DEBUG)

class QbSpider(Spider):
    name = "qb"
    allowed_domains = [ "qiushibaike.com" ]
    start_urls = ["http://www.qiushibaike.com/textnew/" ,]
        
    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="article block untagged mb15"]')
        for question in questions:
            item = QbItem()
            item['author'] = question.xpath('div[@class="author clearfix"]//h2/text()').extract()[0]
            contents = question.xpath('div[@class="content"]')
            con = ''
            for data in contents:
                    con = con + data.xpath('string(.)').extract()[0]
            item['content'] = con
            yield item
        nextpage = Selector(response).xpath('//ul[@class="pagination"]//span[@class="next"]/../@href').extract()[0]
        next_url = 'http://www.qiushibaike.com'+nextpage
        yield scrapy.Request(next_url, self.parse)
#         for url in range(2,9):
            
#         next_url = 'http://www.qiushibaike.com'+nextpage
#         print next_url
#             yield scrapy.Request(first_url+str(url), self.parse)
        #/html/body/div[5]/div/div[1]/ul/li[8]/a/span
# #         if nextpage.startswith(u'/'):
# #         debug("nextpage______:".nextpage)
#         next_url = 'http://www.qiushibaike.com'+nextpage
#         yield scrapy.Request(next_url, self.qb_parse)
    

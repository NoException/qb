
from scrapy import Spider
from scrapy.selector import Selector
from qb.items import QbItem, CommentItem
import scrapy
from _elementtree import Comment
from MySQLdb.constants.FIELD_TYPE import NULL

# def debug(msg):  
#         scrapy.log.msg(msg.decode("utf-8").encode("gb2312"), level=scrapy.log.DEBUG)

class QbSpider(Spider):
    name = "qb"
    allowed_domains = [ "qiushibaike.com" ]
    start_urls = ["http://www.qiushibaike.com/textnew/" ,]
#     start_urls = ["http://www.qiushibaike.com/article/115275820" ,]
        
    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="article block untagged mb15"]')
        for question in questions:
            item = QbItem()
            item['_id'] = question.xpath('@id').extract()[0].split('_')[2]
            item['author'] = question.xpath('div[@class="author clearfix"]//h2/text()').extract()[0]
            contents = question.xpath('div[@class="content"]')
            con = ''
            for data in contents:
                    con = con + data.xpath('string(.)').extract()[0]
            item['content'] = con
            try:
                comments_url = 'http://www.qiushibaike.com'+question.xpath('div[@class="stats"]//a/@href').extract()[0]
                print "----------" + question.xpath('div[@class="stats"]//a/@href').extract()[0]
                yield scrapy.Request(comments_url, meta={'item':item}, callback=self.commen_parse)
            except Exception,e:
                print "bucunzaipinglun"
                yield item
        nextpage = Selector(response).xpath('//ul[@class="pagination"]//span[@class="next"]/../@href').extract()[0]
        next_url = 'http://www.qiushibaike.com'+nextpage
        yield scrapy.Request(next_url, self.parse)
    
    def commen_parse(self, response):
        comments_ = Selector(response).xpath('//div[@class="replay"]')
        item = response.meta['item']
        commentList = []
        for comment in comments_:
            commentItem = CommentItem()
            commentItem['commentuser'] = comment.xpath('a/text()').extract()[0]
            c = comment.xpath('span')
            comm = ''
            for c_ in c:
                comm = comm + c_.xpath('string(.)').extract()[0]
            commentItem['comment'] = comm
            commentList.append(commentItem)
        item['comments'] = commentList
        return item
        
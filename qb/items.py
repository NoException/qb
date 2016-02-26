# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class QbItem(scrapy.Item):
    _id = Field()
    author = Field()
    content = Field()
#     url = Field()
    comments = Field(serializer=str)
    
class CommentItem(scrapy.Item):
    _id = Field()
    commentuser = Field()
    comment = Field()
    
    
    
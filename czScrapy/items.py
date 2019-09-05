# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class czScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    districtName = scrapy.Field()
    keywords = scrapy.Field()
    noticeContent = scrapy.Field()
    noticeContent_html = scrapy.Field()
    noticePubDate = scrapy.Field()
    noticeTitle = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    typeName = scrapy.Field()
    url = scrapy.Field()

    #pass

# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import uuid
import json
from scrapy import cmdline
from czScrapy.mail_utils import *
from czScrapy.items import czScrapyItem

class AppPhSpider(scrapy.Spider):
    name = 'app_ph'
    allowed_domains = ['ph.jxzbtb.cn']
    start_urls = ['http://ph.jxzbtb.cn/jygg/1.html']
    base_url = 'http://ph.jxzbtb.cn'
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    newEndcode = "utf-8"
    #year = time.strftime("%Y", time.localtime())
    newday = ""
    def parse(self, response):
        node_list = response.xpath("//div[@class='ewb-con-bd']/ul/li")
        # newbase_url = response.url[:response.url.rfind("/")] + '/'
        nowItem = 0
        # print(response.url[response.url.rfind('&Paging=')+1:] )
        page_now = int(response.url[response.url.rfind('/') + 1:].split(".")[0])
        typename = ''
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./div/a/@href").extract()[0].encode("utf-8"), 'utf-8').replace("'", "")
            item["id"] = href[href.rfind('/')+1:].split(".")[0]
            item["districtName"] = "平湖市"
            # print(href)

            url = self.base_url + href

            # print(url)
            item["noticePubDate"] = str(
                node.xpath("./span/text()").extract()[0].encode(self.newEndcode),
                'utf-8').replace('[', '').replace(']', '')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]

            item["source"] = "嘉兴平湖市"
            item["title"] = str(node.xpath("./div/a/@title").extract()[0].encode(self.newEndcode), 'utf-8').strip()
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))

            item["typeName"] = "交易公告"

            self.typename = item["typeName"]
            item["url"] = url
            if page_now == 1 and nowItem == 0:
                logging.info(self.typename + "发送email-------")
                send_email(receiver=['16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '嘉兴平湖市招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>嘉兴平湖市招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n",
                                                                                     self.newday))
            nowItem += 1
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)

        if (response.xpath("//li[@class='ewb-page-li ewb-page-hover'][2]/a/text()")):
            # page_now = 2
            page_now += 1
            logging.info(self.typename + "现在爬取第{}页内容".format(page_now))
            # self.nowpage += 1
            newurl = response.url[:response.url.rfind('/') + 1] + str(page_now)+".html"
            print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//div[@class='con']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@class='con']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()
        item["keywords"] = str(
            ''.join(response.xpath("//div[@class='con']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            response.xpath("//h1[@class='infoContentTitle']/text()").extract_first().encode(self.newEndcode), 'utf-8')

        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_ph".split())
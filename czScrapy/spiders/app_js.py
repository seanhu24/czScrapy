# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import uuid
import json
from scrapy import cmdline
from czScrapy.mail_utils import *
from czScrapy.items import czScrapyItem


class AppJsSpider(scrapy.Spider):
    name = 'app_js'
    allowed_domains = ['jszbw.com']
    start_urls = ['http://www.jszbw.com/web/news/newsinfolist.jsp?cId=092BD84429CB0B8771B4EC7AADFCCC7F&start=0' , 'http://www.jszbw.com/web/news/newsinfolist.jsp?cId=9C3CC20867E18B0B5491196F660251AF&start=0']
    base_url= 'http://www.jszbw.com'
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    newEndcode = "utf-8"
    newday = ""

    def parse(self, response):
        node_list = response.xpath("//div[@class='list_info']/div[@class='list_news']")
        # newbase_url = response.url[:response.url.rfind("/")] + '/'
        nowItem = 0
        # print(response.url[response.url.rfind('&Paging=')+1:] )
        page_now = int(int(response.url.split("&")[1].split("=")[1])/20) +1
        typename = ''
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./div/a/@href").extract()[0].encode("utf-8"), 'utf-8').replace("'", "")
            item["id"] = href.split("=")[1]
            item["districtName"] = "嘉善县"
            # print(href)

            url = self.base_url + href

            # print(url)
            item["noticePubDate"] = str(
                node.xpath("./div[2]/text()").extract()[0].encode(self.newEndcode),
                'utf-8').replace('[', '').replace(']', '')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]

            item["source"] = "嘉兴嘉善县"
            item["title"] = str(node.xpath("./div[1]/a/@title").extract()[0].encode(self.newEndcode), 'utf-8').strip()
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            if "092BD84429CB0B8771B4EC7AADFCCC7F" in response.url :
                item["typeName"] = "政府采购最新公告"
            else :
                item["typeName"] = "其他公告资源公告"

            self.typename = item["typeName"]
            item["url"] = url
            if page_now == 1 and nowItem == 0:
                logging.info(self.typename + "发送email-------")
                send_email(receiver=['16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '嘉兴嘉善县招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>嘉兴嘉善县招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n",
                                                                                     self.newday))
            nowItem += 1
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)

        if not (response.xpath("//input[@name='nextPageBtn']/@disabled")):
            # page_now = 2
            page_now += 1
            logging.info(self.typename + "现在爬取第{}页内容".format(page_now))
            # self.nowpage += 1
            newurl = response.url[:response.url.rfind('&') + 1] +"start="+ str((page_now-1)*20)
            print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//div[@class='news_content']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@class='news_content']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()
        item["keywords"] = str(
            ''.join(response.xpath("//div[@class='news_content']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            response.xpath("//div[@class='news_btxx']/text()").extract_first().encode(self.newEndcode), 'utf-8')

        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_js".split())
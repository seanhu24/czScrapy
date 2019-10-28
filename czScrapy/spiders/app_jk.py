# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import uuid
import json
from scrapy import cmdline
from czScrapy.mail_utils import *
from czScrapy.items import czScrapyItem

class AppJkSpider(scrapy.Spider):
    name = 'app_jk'
    allowed_domains = ['jxedz.jiaxing.gov.cn']
    start_urls = ['http://jxedz.jiaxing.gov.cn/Application/Home/news.php?p=1&t=18']
    base_url = 'http://jxedz.jiaxing.gov.cn/Application/Home/'
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    newEndcode = "utf-8"
    newday = ""
    typename = ''
    def parse(self, response):
        node_list = response.xpath("//div[@id='ggfl']/div/dl")
        # newbase_url = response.url[:response.url.rfind("/")] + '/'
        nowItem = 0
        # print(response.url[response.url.rfind('&Paging=')+1:] )
        page_now = int(response.url.split("&")[0].split("=")[1])
        typename = ''
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./dt/a/@href").extract()[0].encode("utf-8"), 'utf-8').replace("'", "")
            if  "=" not in href :
                continue
            item["id"] = href.split("=")[1]
            item["districtName"] = "经济开发区"
            # print(href)

            url = self.base_url + href

            # print(url)
            item["noticePubDate"] = str(
                node.xpath("./dd/text()").extract()[0].encode(self.newEndcode),
                'utf-8').replace('[', '').replace(']', '')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]

            item["source"] = "嘉兴经济开发区"
            item["title"] = str(node.xpath("./dt/a/text()").extract()[0].encode(self.newEndcode), 'utf-8').strip()
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))

            item["typeName"] = "通知公告"


            self.typename = item["typeName"]
            item["url"] = url
            if page_now == 1 and nowItem == 0:
                logging.info(self.typename + "发送email-------")
                send_email(receiver=['16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '嘉兴经济开发区招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>嘉兴经济开发区招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n",
                                                                                     self.newday))
            nowItem += 1
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)

        if "disabled" not in (str(response.xpath("//div[@class='pagelist']/a[last()]/@class").extract_first().encode(self.newEndcode), 'utf-8')):
            # page_now = 2
            page_now += 1
            logging.info(self.typename + "现在爬取第{}页内容".format(page_now))
            # self.nowpage += 1
            newurl = response.url[:response.url.rfind('p=') ] + "p=" + str(page_now ) + "&t=18"
            print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//div[@class='newshow-txt']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@class='newshow-txt']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()
        item["keywords"] = str(
            ''.join(response.xpath("//div[@class='newshow-txt']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            response.xpath("//div[@class='newshow']/h4/text()").extract_first().encode(self.newEndcode), 'utf-8').strip()

        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_jk".split())
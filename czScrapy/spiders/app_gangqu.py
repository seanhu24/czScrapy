# -*- coding: utf-8 -*-
import scrapy
from czScrapy.items import czScrapyItem
import logging
import time
import uuid
import json
from scrapy import cmdline
from czScrapy.mail_utils import *
from scrapy.selector import Selector
from urllib.parse import urlencode, urlparse, parse_qs


class AppGangQuSpider(scrapy.Spider):
    name = 'app_gangqu'
    allowed_domains = ['jiaxing.gov.cn']
    newEndcode = "utf-8"
    new_url='http://jxgq.jiaxing.gov.cn'
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    urls = ['jxgq.jiaxing.gov.cn/col/col1591223/index.html?uid=4922258&pageNum=1','jxgq.jiaxing.gov.cn/col/col1591223/index.html?uid=4922259&pageNum=1','jxgq.jiaxing.gov.cn/col/col1591224/index.html?uid=4922298&pageNum=1','jxgq.jiaxing.gov.cn/col/col1591224/index.html?uid=4922299&pageNum=1']
    def start_requests(self):
        for url in self.urls:
            columnid=url.split('/')[2].replace('col','')
            unitid =url.split('&')[0].split('=')[1]
        #logging.info("现在爬取第{}页内容".format(self.nowpage))
            yield scrapy.FormRequest(
                url='http://jxgq.jiaxing.gov.cn/module/jpage/dataproxy.jsp?startrecord=0&endrecord=100000&perpage=999',
                formdata={
                # 'infotypeId': '0',  # 这里不能给bool类型的True，requests模块中可以
                'appid': '1',  # 这里不能给int类型的1，requests模块中可以
                'col': '1',
                'columnid': columnid,
                'path': '/',
                'permissiontype': '0',
                'sourceContentType': '1',
                'unitid': unitid,
                'webid': '3177',
                'webname': '嘉兴港区开发建设管理委员会，嘉兴港区综合保税区管理委员会'
                },  # 这里的formdata相当于requ模块中的data，key和value只能是键值对形式
                callback=self.parse
            )
    def parse(self, response):
        print(response.text)
        text = response.text.replace('<![CDATA[', '').replace(']]>', '')
        sel = scrapy.Selector(text=text)
        node_list = sel.xpath("//record/li")
        #node_list = response.xpath("//record/tr")

        newbase_url = response.url
        nowItem = 0
        typename = ''
        page_now=1

        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./a/@href").extract()[0].encode(self.newEndcode), self.newEndcode)
            #print(href)
            item["id"] = href.split('_')[2].split('.')[0]
            item["districtName"] = "港区"

            url = self.new_url+href.replace("'", "")
            #print(url)

            item["noticePubDate"] = str(node.xpath("./span/text()").extract()[0].encode(self.newEndcode),
                                        'utf-8').strip()
            # item["noticeTitle"] = self.new_item["noticeTitle"]

            self.newday = item["noticePubDate"]
            item["source"] = "嘉兴港区"
            item["title"] = str(node.xpath("./a/@title").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))

            item["typeName"] = "招标-中标公告"
            typename = item["typeName"]
            item["url"] = url
            #page_now = int(response.url.split('&')[1].split('=')[1])
            if (page_now == 1) and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=['16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '嘉兴港区',
                           cont='<h1>今日爬取地址{}\r\n<br>嘉兴港区最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1
            page_now += 1

            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
    def newparse(self, response):
        #print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        #print(item)
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//div[@class='box_wzy_ys']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@class='box_wzy_ys']//*/text()").extract()).encode(self.newEndcode), 'utf-8').strip()
        item["keywords"] = str(''.join(response.xpath("//div[@class='box_wzy_ys']//*/text()").extract()).encode(self.newEndcode),
                               'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            ''.join(response.xpath("//div[@class='main-fl-tit']/text()").extract()).encode(self.newEndcode), 'utf-8').strip()
        # print(item)
        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_gangqu".split())
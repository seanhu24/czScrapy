# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
from czScrapy.items import czScrapyItem
import logging
from czScrapy.mail_utils import *

import os
import time


class AppYcSpider(scrapy.Spider):
    name = 'app_yc'
    allowed_domains = ['sxyc.gov.cn']
    #start_urls = ['http://www.sxyc.gov.cn/col/col1559789/index.html?uid=4851098&pageNum=2','http://www.sxyc.gov.cn/module/jpage/dataproxy.jsp?page=1&appid=1&appid=1&webid=3090&path=/&columnid=1559789&unitid=4851098&webname=%E7%BB%8D%E5%85%B4%E5%B8%82%E8%B6%8A%E5%9F%8E%E5%8C%BA%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C%EF%BC%88%E9%AB%98%E6%96%B0%E5%8C%BA%E3%80%81%E8%A2%8D%E6%B1%9F%E5%BC%80%E5%8F%91%E5%8C%BA%E7%AE%A1%E5%A7%94%E4%BC%9A%EF%BC%89&permissiontype=0']
    urls = ['www.sxyc.gov.cn/col/col1559789/index.html?uid=4851098&pageNum=1','www.sxyc.gov.cn/col/col1559790/index.html?uid=4851098&pageNum=1']
    base_url ='http://www.sxyc.gov.cn'
    logging.info("开始爬取绍兴市越城区人民政府（高新区、袍江开发区管委会）----")
    newEndcode="utf-8"

    def start_requests(self):
        headers = {
            "Referer": "http://www.sxyc.gov.cn/col/col1559789/index.html?uid=4851098&pageNum=1"
        }
        for url in self.urls:
            columnid=url.split('/')[2].replace('col','')
            unitid =url.split('&')[0].split('=')[1]
        #logging.info("现在爬取第{}页内容".format(self.nowpage))
            yield scrapy.FormRequest(
                url='http://www.sxyc.gov.cn/module/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15',
                headers=headers,
                formdata={
                # 'infotypeId': '0',  # 这里不能给bool类型的True，requests模块中可以
                'appid': '1',  # 这里不能给int类型的1，requests模块中可以
                'col': '1',
                'columnid': columnid,
                'path': '/',
                'permissiontype': '0',
                'sourceContentType': '1',
                'unitid': unitid,
                'webid': '3090',
                'webname': '绍兴市越城区人民政府'
                },  # 这里的formdata相当于requ模块中的data，key和value只能是键值对形式
                callback=self.parse
            )
    #print(local_path)
    # 实例化一个浏览器对象

    def parse(self, response):
        print(response.text)
        text = response.text.replace('<![CDATA[', '').replace(']]>', '')
        sel = scrapy.Selector(text=text)
        node_list = sel.xpath("//record/li")
        # node_list = response.xpath("//record/tr")

        newbase_url = response.url
        nowItem = 0
        typename = ''
        page_now = 1
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./a/@href").extract()[0].encode(self.newEndcode), self.newEndcode)
            # print(href)
            item["id"] = href.split('_')[2].split('.')[0]
            item["districtName"] = "越城区"

            url = href.replace("'", "")
            # print(url)

            item["noticePubDate"] = str(node.xpath("./span/text()").extract()[0].encode(self.newEndcode),
                                        'utf-8').strip()
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "绍兴市越城区"
            item["title"] = str(node.xpath("./a/@title").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))

            item["typeName"] = "采购-成交公告"
            typename = item["typeName"]
            item["url"] ="http://www.sxyc.gov.cn"+ url
            page_now = int(response.url.split('&')[1].split('=')[1])
            if (page_now == 1) and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=['16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '绍兴市越城区',
                           cont='<h1>今日爬取地址{}\r\n<br>绍兴市越城区最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1
            page_now += 1
            yield scrapy.Request("http://www.sxyc.gov.cn"+ url, meta={'item': item}, callback=self.newparse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//div[@id='zoom']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@id='zoom']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()
        item["keywords"] = str(
            ''.join(response.xpath("//div[@id='zoom']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            ''.join(response.xpath("//p[@class='con-title']/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()
        # print(item)
        yield item



if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_yc".split())
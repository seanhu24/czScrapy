# -*- coding: utf-8 -*-
import scrapy
from czScrapy.items import czScrapyItem
import logging
import time
import uuid
from czScrapy.mail_utils import *
from scrapy import cmdline

class AppXzSpider(scrapy.Spider):
    name = 'app_xz'
    allowed_domains = ['jxxzztb.com']
    start_urls = ['http://www.jxxzztb.com/zbgg/index.htm', 'http://www.jxxzztb.com/zbgs/index.htm', 'http://www.jxxzztb.com/zjdxx/index.htm']
    base_url = 'http://www.jxxzztb.com'
    newEndcode = 'utf-8'
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def parse(self, response):
        node_list = response.xpath("//div[@class='Rg03 FloatL']/dl/dt")
        newbase_url = response.url[:response.url.rfind("/")] + '/'
        nowItem = 0
        page_len = len(response.url.split("_"))
        typename = ''
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./a/@href").extract()[0].encode("utf-8"), 'utf-8').replace("'", "")
            item["id"] = href[href.rfind("/")+1:].split(".")[0]
            item["districtName"] = "秀洲区"
            #print(href)

            url = self.base_url + href
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
            #print(url)
            item["noticePubDate"] = str(node.xpath("./font/text()").extract()[0].encode(self.newEndcode), 'utf-8')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "嘉兴秀洲区"
            item["title"] = str(node.xpath("./a/text()").extract()[0].encode(self.newEndcode), 'utf-8').strip()
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            if 'zbgg' in response.url :
                item["typeName"] = "招标公告"
            elif 'zbgs' in response.url :
                item["typeName"] = "中标公示"
            else:
                item["typeName"] = "镇街道信息"
            self.typename= item["typeName"]
            item["url"] = url
            if page_len == 1 and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=[ '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '嘉兴秀洲区招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>嘉兴秀洲区招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1
            yield item

        if not (response.xpath("//div[@class='Rg02 FloatL']/div[2]/div/a[3]/@disabled")):
            page_now = 2
            if page_len > 1:
                page_now = int(response.url.split("_")[1].split(".")[0])+1
            logging.info(self.typename+"现在爬取第{}页内容".format(page_now))
            #self.nowpage += 1
            newurl = newbase_url + 'index_' + str(page_now) + '.htm'
            print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
                ''.join(response.xpath("//div[@class='Rg06 floatL']").extract()).encode(self.newEndcode),
                'utf-8')
        item["noticeContent"] = str(''.join(response.xpath("//div[@class='Rg06 floatL']//*/text()").extract()).encode(self.newEndcode), 'utf-8').strip()
        item["keywords"] = str(''.join(response.xpath("//div[@class='Rg06 floatL']//*/text()").extract()).encode(self.newEndcode), 'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            response.xpath("//div[@class='Rg06 floatL']/font/text()").extract_first().encode(self.newEndcode), 'utf-8')
        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_xz".split())

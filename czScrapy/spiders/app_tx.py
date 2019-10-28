# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import uuid
import json
from scrapy import cmdline
from czScrapy.mail_utils import *
from czScrapy.items import czScrapyItem

class AppTxSpider(scrapy.Spider):
    name = 'app_tx'
    allowed_domains = ['ztb.txggfw.cn']
    start_urls = ['http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?title=&startdate=&enddate=&categoryNum=008001&Paging=1']
    base_url ='http://ztb.txggfw.cn'
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    newEndcode="utf-8"
    year = time.strftime("%Y", time.localtime())
    def parse(self, response):
        node_list = response.xpath("//ul[@class='ewb-dynamic-list']/li")
        #newbase_url = response.url[:response.url.rfind("/")] + '/'
        nowItem = 0
        #print(response.url[response.url.rfind('&Paging=')+1:] )
        page_now = int(response.url[response.url.rfind('&Paging=')+1:].split("=")[1] )
        typename = ''
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./a/@href").extract()[0].encode("utf-8"), 'utf-8').replace("'", "")
            item["id"] = href.split('&')[0].split("=")[1]
            item["districtName"] = "桐乡市"
            # print(href)

            url = self.base_url + href

            # print(url)
            self.newday =self.year+'-'+ str(node.xpath("./span/text()").extract()[0].encode(self.newEndcode), 'utf-8')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            #self.newday = item["noticePubDate"]
            item["source"] = "嘉兴桐乡市"
            item["title"] = str(node.xpath("./a/@title").extract()[0].encode(self.newEndcode), 'utf-8').strip()
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))

            item["typeName"] = "一般公告"
            self.typename = item["typeName"]
            item["url"] = url
            if page_now == 1 and nowItem == 0:
                logging.info(self.typename+"发送email-------")
                send_email(receiver=['16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '嘉兴桐乡市招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>嘉兴桐乡市招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n",
                                                                                     self.newday))
            nowItem += 1
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)

        if  (response.xpath("//td[@class='pageout'][3]/@onclick")):
            #page_now = 2
            page_now +=1
            logging.info(self.typename + "现在爬取第{}页内容".format(page_now))
            # self.nowpage += 1
            newurl = response.url[:response.url.rfind('&Paging=')]+'&Paging='+str(page_now)
            print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//div[@class='article-block']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@class='article-block']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()
        item["keywords"] = str(
            ''.join(response.xpath("//div[@class='article-block']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            response.xpath("//h2[@class='article-title']/text()").extract_first().encode(self.newEndcode), 'utf-8')
        newtime_xp= str(
            response.xpath("//div[@class='info-sources']/text()").extract_first().encode(self.newEndcode), 'utf-8')


        newtime_xp=newtime_xp[newtime_xp.find("信息时间："):newtime_xp.find("阅读次数")].replace("信息时间：","").strip()
        item["noticePubDate"]= time.strftime("%Y-%m-%d", time.strptime(newtime_xp, "%Y/%m/%d"))
        yield item

if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_tx".split())
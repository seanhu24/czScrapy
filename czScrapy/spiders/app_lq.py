# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import uuid
import json
from scrapy import cmdline
from czScrapy.mail_utils import *
from czScrapy.items import czScrapyItem
from scrapy.selector import Selector
from urllib.parse import urlencode, urlparse, parse_qs
class AppLqSpider(scrapy.Spider):
    name = 'app_lq'
    allowed_domains = ['www.luqiao.gov.cn','zjzfcg.gov.cn']
    start_urls = ['http://www.luqiao.gov.cn/InfoPub/ArticleList.aspx?CategoryID=528&CurrentPageIndex=1']
    base_url ='http://www.luqiao.gov.cn'
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    newEndcode = "utf-8"
    newday = ""
    typename = ''
    def parse(self, response):
        node_list = response.xpath("//div[@class='ListItem']")
        # newbase_url = response.url[:response.url.rfind("/")] + '/'
        nowItem = 0
        # print(response.url[response.url.rfind('&Paging=')+1:] )
        page_now = int(response.url.split("&")[1].split("=")[1])
        typename = ''
        #print(response.url)
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./div[@class='NoWrapHidden ListItemTitle']/a/@href").extract()[0].encode("utf-8"), 'utf-8').replace("'", "")
            #print(href)
            if '=' not in href :
                continue
            item["id"] = href.split("=")[1]
            item["districtName"] = "路桥区"
            #print(href)

            url = href

            #print(url)
            item["noticePubDate"] = str(
                node.xpath("./div[@class='ListItemDate']/text()").extract()[0].encode(self.newEndcode),
                'utf-8').strip().replace('[', '').replace(']', '')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]

            item["source"] = "台州路桥区"
            item["title"] = str(node.xpath("./div[@class='NoWrapHidden ListItemTitle']/a/@title").extract()[0].encode(self.newEndcode), 'utf-8').strip()
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))

            item["typeName"] = "投标公告"

            self.typename = item["typeName"]
            item["url"] = url
            if page_now == 1 and nowItem == 0:
                logging.info(self.typename + "发送email-------")
                send_email(receiver=['16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '台州路桥区招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>台州路桥区招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n",
                                                                                       self.newday))
            nowItem += 1
           # yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
            if 'InfoPub' in href:
                item["url"] = self.base_url+url
                yield scrapy.Request(self.base_url+url, meta={'item': item}, callback=self.newparse)
            elif 'zjzfcg' in href:
                #item["id"] = href[href.index('=') + 1:]
                para = {
                    'noticeId': item["id"],
                    # 'url': 'http://notice.zcygov.cn/new/noticeDetail'
                    'url': 'noticeDetail'
                }
                url = 'http://manager.zjzfcg.gov.cn/cms/api/cors/remote/results?'+ urlencode(para)
                yield scrapy.Request(url, meta={'item': item}, callback=self.newparse_zf)
            else:
                continue

        if not response.xpath("//*[@id='AspNetPager1']/div[2]/a[11]/@disabled"):
            # page_now = 2
            page_now += 1
            logging.info(self.typename + "现在爬取第{}页内容".format(page_now))
            # self.nowpage += 1
            newurl = response.url[:response.url.rfind('&')+1] + "CurrentPageIndex=" + str(page_now)
            print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)


    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//td[@class='TemplateTd']").extract()).encode(self.newEndcode), 'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//td[@class='TemplateTd']//*/text()").extract()).encode(self.newEndcode),
            'utf-8')
        item["keywords"] = str(
            ''.join(response.xpath("//td[@class='TemplateTd']//*/text()").extract()).encode(self.newEndcode),
            'utf-8')[:100]
        item["noticeTitle"] = str(
            ''.join(response.xpath("//div[@class='Main']/div[2]/div/div/div[1]/text()").extract()).strip().encode(self.newEndcode), 'utf-8')
        print(item)
        yield item

    def newparse_zf(self, response):
        print(response.text)
        res = json.loads(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = res.get("noticeContent")
        item["noticeContent"] = str(
            ''.join(''.join(Selector(text=res.get("noticeContent")).xpath("string(//div)").extract()).split()).encode(
                self.newEndcode), 'utf-8')
        item["keywords"] = str(
            ''.join(''.join(Selector(text=res.get("noticeContent")).xpath("string(//div)").extract()).split()).encode(
                self.newEndcode), 'utf-8')[:100]
        item["noticeTitle"] = res.get("noticeTitle")
        print(item)
        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_lq".split())
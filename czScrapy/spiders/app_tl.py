# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import uuid
import json
from scrapy import cmdline
from czScrapy.mail_utils import *
from czScrapy.items import czScrapyItem
class AppTlSpider(scrapy.Spider):
    name = 'app_tl'
    allowed_domains = ['tonglu.gov.cn']
    start_urls = ['http://www.tonglu.gov.cn/module/xxgk/search.jsp?divid=div1551660&infotypeId=70&jdid=3024&area=%20&sortfield=&currpage=1']
    logging.info("开始爬取杭州桐庐----")
    totlepage = 1
    nowpage = 1
    newEndcode = "utf-8"
    newday = ""
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logging.info("现在爬取第{}页内容".format(nowpage))

    def parse(self, response):
        #print(response.text)
        node_list = response.xpath("//table//tr[position()>1]")
        self.totlepage = int(response.xpath("//table[@class='tb_title']//td[2]/a[last()]/text()").extract()[0].encode(self.newEndcode))
        #newbase_url = response.url[:response.url.rfind("/")] + '/'
        nowItem = 0
        #print(node_list)
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./td[2]/a/@href").extract()[0].encode("utf-8")).replace("'", "")[1:]
            item["id"] = href.split('_')[2].split('.')[0]
            item["districtName"] = "桐庐县"
            # print(href)

            url =href
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
            item["noticePubDate"] = str(node.xpath("./td[4]/text()").extract()[0].encode(self.newEndcode), 'utf-8')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "杭州桐庐县门户网站"
            item["title"] = str(node.xpath("./td[2]/a/@title").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            item["typeName"] = "招标公告"
            item["url"] = url
            if self.nowpage == 0 and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=[ '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '杭州桐庐县招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>杭州桐庐县招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1
            yield item

        if self.nowpage < self.totlepage:
            logging.info("现在爬取第{}页内容".format(self.nowpage + 1))
            self.nowpage += 1
            newurl = response.url[:response.url.index('&currpage=')+1] + 'currpage=' + str(self.nowpage)
            print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
                ''.join(response.xpath("//div[@class='xxgk_t_con']").extract()).encode(self.newEndcode),
                'utf-8')
        item["noticeContent"] = str(''.join(response.xpath("//div[@class='xxgk_t_con']//*/text()").extract()).encode(self.newEndcode), 'utf-8')
        item["keywords"] = str(''.join(response.xpath("//div[@class='xxgk_t_con']//*/text()").extract()).encode(self.newEndcode), 'utf-8')[:100]

        item["noticeTitle"] = str(
            response.xpath("//div[@class='xxgk_t_til']/text()").extract_first().encode(self.newEndcode), 'utf-8')
        yield item


if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_tl".split())
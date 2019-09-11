# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
from czScrapy.items import czScrapyItem
import logging
from czScrapy.mail_utils import *
import time

class AppKqSpider(scrapy.Spider):
    name = 'app_kq'
    allowed_domains = ['sxxztb.gov.cn']
    logging.info("开始爬取绍兴市柯桥区公共资源交易中心----")
    start_urls = ['http://www.sxxztb.gov.cn/Bulletin/viewmore1.aspx?BulletinTypeId=51&frontid=5&pageindex=1','http://www.sxxztb.gov.cn/Bulletin/viewmore1.aspx?BulletinTypeId=52&frontid=5&pageindex=1']
    base_url ='http://www.sxxztb.gov.cn/Bulletin'
    totlepage = 1
    nowpage = 1
    newEndcode = "utf-8"

    def parse(self, response):
        #print(response.status)
        if self.nowpage% 10 :
            time.sleep(1)
        node_list = response.xpath("//div[@class='roundin']/table[2]//table")
        if self.nowpage == 1 :
            self.totlepage = int(response.xpath("//select[@name='fey']/option[last()]/text()").extract()[0].encode(self.newEndcode))
        #newbase_url = response.url[:response.url.rfind("/")] + '/'

        nowItem = 0
        for node in node_list:
            item = czScrapyItem()
            if not node.xpath("//td[2]/a/@href").extract()[0].encode("utf-8"):
                time.sleep(1)
            href = str(node.xpath("//td[2]/a/@href").extract()[0].encode("utf-8"),'utf-8').replace("../Bulletin", "")
            item["id"] = href.split('=')[1]
            item["districtName"] = "柯桥区"
            # print(href)

            url = self.base_url + href
            #print(url)
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
            #item["noticePubDate"] = str(node.xpath("//tr/td[3]/text()").extract()[0].encode(self.newEndcode), 'utf-8')

            # item["noticeTitle"] = self.new_item["noticeTitle"]

            item["source"] = "绍兴市柯桥区公共资源交易中心"
            item["title"] = str(node.xpath("//td[2]/a/text()").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            if 'BulletinTypeId=51' in response.url :
                item["typeName"] = "交易公告"
            else:
                item["typeName"] = "成交结果"
            item["url"] = url
            if self.nowpage == 0 and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=['huxiao_hz@citicbank.com', '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '绍兴市柯桥区公共资源交易中心',
                           cont='<h1>今日爬取地址{}\r\n<br>绍兴市柯桥区公共资源交易中心最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1
            yield item

        if self.nowpage < self.totlepage:
            logging.info("现在爬取第{}页内容".format(self.nowpage + 1))
            self.nowpage += 1
            newurl = response.url[:response.url.rfind("=")+1] + str(self.nowpage)
            print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']

        noticePubDate= str(
            response.xpath("// span[@id='lblPublishDate']/text()").extract()[0].encode(self.newEndcode),
            'utf-8').replace("发布时间：", "")
        item["noticePubDate"] = noticePubDate[:noticePubDate.rfind("阅")].strip()
        print('日期' + item["noticePubDate"])
        self.newday = item["noticePubDate"]

        item["noticeContent_html"] = str(
            ''.join(response.xpath("//span[@id='lblContent']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//span[@id='lblContent']//*/text()").extract()).encode(self.newEndcode), 'utf-8')
        item["keywords"] = str(''.join(response.xpath("//span[@id='lblContent']//*/text()").extract()).encode(self.newEndcode),
                               'utf-8')[:100]
        item["noticeTitle"] = str(
            response.xpath("//span[@id='lblTitle']/text()").extract_first().encode(self.newEndcode), 'utf-8')
        # print(item)
        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_kq".split())
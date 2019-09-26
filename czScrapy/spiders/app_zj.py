# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
from czScrapy.items import czScrapyItem
import logging
from czScrapy.mail_utils import *
class AppZjSpider(scrapy.Spider):
    name = 'app_zj'
    allowed_domains = ['ggb.zhuji.gov.cn']
    start_urls = ['http://ggb.zhuji.gov.cn/TPFront/ggdf/037001/?Paging=1','http://ggb.zhuji.gov.cn/TPFront/ggdf/037002/?Paging=1','http://ggb.zhuji.gov.cn/TPFront/ggdf/037003/?Paging=1','http://ggb.zhuji.gov.cn/TPFront/ggdf/037004/?Paging=1','http://ggb.zhuji.gov.cn/TPFront/ggdf/037005/?Paging=1']
    base_url = 'http://ggb.zhuji.gov.cn'
    newEndcode ='utf-8'
    logging.info("开始爬取绍兴诸暨----")
    typename =''
    def parse(self, response):
        #print(response.text)
        node_list = response.xpath("//div[@class='column border mt10']/div[2]/div[1]//*/tr")
        #print(node_list)
        nowItem = 0
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./td/a/@href").extract()[0].encode(self.newEndcode), self.newEndcode)
            item["id"] = href.split('&')[0].split('=')[1]
            item["districtName"] = "诸暨市"
            #print(href)

            url = self.base_url + href.replace("'", "")
            #print(url)
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
            item["noticePubDate"] = str(node.xpath("./td[@align='right']/text()").extract()[0].encode(self.newEndcode),
                                        'utf-8').replace('[', '').replace(']', '')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "诸暨市公共资源交易网"
            item["title"] = str(node.xpath("./td/a/@title").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            if '037001' in response.url:
                item["typeName"] = "要素公示"
            elif '037002' in response.url:
                item["typeName"] = "采购公告"
            elif '037003' in response.url:
                item["typeName"] = "成交公示"
            elif '037004' in response.url:
                item["typeName"] = "成交结果"
            else:
                item["typeName"] = "合同公告"
            item["url"] = url
            self.typename =item["typeName"]
            if (response.url.split('=')[1] == 1)and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=[ '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '诸暨市公共资源交易网',
                           cont='<h1>今日爬取地址{}\r\n<br>诸暨市公共资源交易网最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1
            yield item

        if response.xpath("//td[@class='pageout'][3]/@onclick"):
            page =int(response.url.split('=')[1])
            logging.info(self.typename+"现在爬取第{}页内容".format(str(page+1)))
            #print(str(self.nowpage)+'-----'+response.url)
            page+=1
            newurl = response.url[:response.url.index('=') + 1] + str(page)
            # print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)


    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//td[@class='infodetail']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//td[@class='infodetail']//*/text()").extract()).encode(self.newEndcode), 'utf-8').strip()
        item["keywords"] = str(''.join(response.xpath("//td[@class='infodetail']//*/text()").extract()).encode(self.newEndcode),
                               'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            response.xpath("//div[@class='positive-content-hd']/text()").extract_first().encode(self.newEndcode), 'utf-8').strip()
        # print(item)
        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_zj".split())

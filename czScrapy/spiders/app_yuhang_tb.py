# -*- coding: utf-8 -*-
import scrapy
from czScrapy.items import czScrapyItem
import logging
import time
import uuid
from czScrapy.mail_utils import *
from scrapy import cmdline
class AppYuhangTbSpider(scrapy.Spider) :
    logging.info("----开始爬取杭州余杭政府门户网站-------")
    name = 'app_yuhang_tb'
    allowed_domains = ['www.yuhang.gov.cn']
    base_url = "http://www.yuhang.gov.cn/xxgk/gggs/zbgg/zfcg/"
    base_url2 = 'http://www.yuhang.gov.cn/xxgk/gggs/zbggs/zfcg1/'
    start_urls = [base_url, base_url2]
    totlepage = 1
    nowpage = 0
    newEndcode="utf-8"
    newday = ""
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logging.info("现在爬取第{}页内容".format(nowpage))
    def parse(self, response):
       node_list = response.xpath("//tr[@class='ZjYhN018']")
       self.totlepage = int(response.xpath("//strong[3]/text()").extract()[0].encode(self.newEndcode))
       newbase_url=response.url[:response.url.rfind("/")]+'/'
       nowItem = 0
       for node in node_list:
           item = czScrapyItem()
           href = str(node.xpath("./td/a[2]/@href").extract()[0].encode("utf-8")).replace("'", "")[1:]
           item["id"] = href.split('_')[1].split('.')[0]
           item["districtName"] = "余杭区"
           #print(href)

           url = newbase_url+href
           yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
           item["noticePubDate"] = str(node.xpath("./td[3]/text()").extract()[0].encode(self.newEndcode), 'utf-8')
           #item["noticeTitle"] = self.new_item["noticeTitle"]
           self.newday = item["noticePubDate"]
           item["source"] = "杭州余杭政府门户网站"
           item["title"] = str(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode), 'utf-8')
           #print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
           item["typeName"] = "招标公告"
           item["url"] = url
           if self.nowpage == 0 and nowItem == 0:
               logging.info("发送email-------")
               send_email(receiver=['huxiao_hz@citicbank.com', '16396355@qq.com', '8206741@163.com'],
               #send_email(receiver=['8206741@163.com'],
                          title=self.curr_time+'杭州余杭政府门户网站'+str(uuid.uuid1()), cont='<h1>今日爬取地址{}\r\n<br>杭州余杭政府门户网站最新更新日期是{}</h1>'.format(response.url+"\r\n", self.newday))
           nowItem+=1
           yield item

       if  self.nowpage < self.totlepage:
           logging.info("现在爬取第{}页内容".format(self.nowpage+1))
           self.nowpage += 1
           newurl = newbase_url+'index_'+ str(self.nowpage)+'.html'
           yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        #print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        xpathtxt = "//table[@class='ZjYhN019 ZjYhN020']//p/text()"
        if response.xpath(xpathtxt) :
            item["noticeContent_html"] = str(''.join(response.xpath("//table[@class='ZjYhN019 ZjYhN020']//p").extract()).encode(self.newEndcode), 'utf-8')
            item["noticeContent"] = str(''.join(response.xpath(xpathtxt).extract()).encode(self.newEndcode), 'utf-8')
            item["keywords"] = str(''.join(response.xpath(xpathtxt).extract()).encode(self.newEndcode), 'utf-8')[:100]
        else :
            xpathtxt2 = "//table[@class='ZjYhN019 ZjYhN020']//span/text()"
            item["noticeContent_html"] = str(''.join(response.xpath("//table[@class='ZjYhN019 ZjYhN020']//span").extract()).encode(self.newEndcode), 'utf-8')
            item["noticeContent"] = str(''.join(response.xpath(xpathtxt2).extract()).encode(self.newEndcode), 'utf-8')
            item["keywords"] =str( ''.join(response.xpath(xpathtxt2).extract()).encode(self.newEndcode), 'utf-8')[:100]
        item["noticeTitle"] = str(response.xpath("//td[@class='GgFwN015']/text()").extract_first().encode(self.newEndcode), 'utf-8')
        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_yuhang_tb".split())

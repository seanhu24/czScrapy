# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
from czScrapy.items import czScrapyItem
import logging
from czScrapy.mail_utils import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import platform
#无头浏览器设置
chorme_options = Options()
chorme_options.add_argument("--headless")
chorme_options.add_argument("--disable-gpu")
chorme_options.add_argument('--no-sandbox')
# prefs = {'profile.managed_default_content_settings.images': 2}
# options.add_experimental_option('prefs', prefs)
chorme_options.add_argument('--disable-java')
chorme_options.add_argument('--blink-settings=imagesEnabled=false')

class AppAjSpider(scrapy.Spider):
    name = 'app_aj'
    allowed_domains = ['ajztb.com']
    start_urls = ['http://www.ajztb.com/jyxx/003002/moreinfo.html']
    base_url = 'http://www.ajztb.com'
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    newEndcode = "utf-8"
    total_page =1
    newEndcode = "utf-8"
    if 'Linux' in platform.system():
        chromeName = 'chromedriver'
    else:
        chromeName = 'chromedriver.exe'
    local_path = os.path.abspath(chromeName)
    #year = time.strftime("%Y", time.localtime())
    newday = ""
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chorme_options, executable_path=self.local_path)
        super().__init__()

    # 整个爬虫结束后关闭浏览器
    def close(self, spider):
        logging.info("结束杭州财政的爬取---")
        self.browser.quit()
    def parse(self, response):
        #print(response.text)
        node_list = response.xpath("//ul[@class='ewb-notice-items']/li")
        # newbase_url = response.url[:response.url.rfind("/")] + '/'
        nowItem = 0
        # print(response.url[response.url.rfind('&Paging=')+1:] )
        page_td = response.url[response.url.rfind('/') + 1:].split(".")[0]
        if 'moreinfo' in page_td :
            page_now = 1
        else :
            page_now = int(page_td)
        if page_now == 1:
            self.total_page = int(''.join(
                response.xpath("//div[@id='page']/ul[@class='m-pagination-page']/li[last()]/a/text()").extract()).encode(self.newEndcode))-1
        print(self.total_page)
        #print(response.xpath("//div[@id='page']/ul[@class='m-pagination-page']/li[last()]"))
        typename = ''
        for node in node_list:
            item = czScrapyItem()

            href = str(node.xpath("./a/@href").extract()[0].encode("utf-8"), 'utf-8').replace("'", "")
            item["id"] = href[href.rfind('/')+1:].split(".")[0]
            item["districtName"] = "安吉县"
            # print(href)

            url = self.base_url + href

            # print(url)
            item["noticePubDate"] = str(
                node.xpath("./span/text()").extract()[0].encode(self.newEndcode),
                'utf-8').replace('[', '').replace(']', '')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]

            item["source"] = "湖州安吉县"
            item["title"] = str(node.xpath("./a/@title").extract()[0].encode(self.newEndcode), 'utf-8').strip()
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))

            item["typeName"] = "政府采购"

            self.typename = item["typeName"]
            item["url"] = url
            if page_now == 1 and nowItem == 0:
                logging.info(self.typename + "发送email-------")
                send_email(receiver=['16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '湖州安吉县招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>湖州安吉县招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n",
                                                                                     self.newday))
            nowItem += 1
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)

        if page_now <self.total_page:
            # page_now = 2
            page_now += 1
            logging.info(self.typename + "现在爬取第{}页内容".format(page_now))
            # self.nowpage += 1
            newurl = response.url[:response.url.rfind('/') + 1] + str(page_now)+".html"
            print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//div[@id='infocontent']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@id='infocontent']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()
        item["keywords"] = str(
            ''.join(response.xpath("//div[@id='infocontent']//*/text()").extract()).encode(self.newEndcode),
            'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            response.xpath("//div[@class='detail-tt']/text()").extract_first().encode(self.newEndcode), 'utf-8')

        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_aj".split())
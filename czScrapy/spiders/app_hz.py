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
class AppHzSpider(scrapy.Spider):
    name = 'app_hz'
    allowed_domains = ['hangzhou.gov.cn']
    start_urls = ['http://czj.hangzhou.gov.cn/col/col1651779/index.html?uid=4984880&pageNum=1', 'http://czj.hangzhou.gov.cn/col/col1651780/index.html?uid=4984880&pageNum=1']
    base_url = 'http://czj.hangzhou.gov.cn'
    logging.info("开始爬取杭州财政----")
    #totlepage_146 = 1
    #totlepage_149 = 1
    #nowpage_146 = 1
    #nowpage_149 = 1
    newEndcode = "utf-8"

    if 'Linux' in platform.system():
        chromeName = 'chromedriver'
    else:
        chromeName = 'chromedriver.exe'
    local_path = os.path.abspath(chromeName)
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(local_path)
    # 实例化一个浏览器对象
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chorme_options, executable_path=self.local_path)
        super().__init__()

    # 整个爬虫结束后关闭浏览器
    def close(self, spider):
        logging.info("结束杭州财政的爬取---")
        self.browser.quit()

    def parse(self, response):
        #print(response.text)
        typename = ''
        node_list = response.xpath("//div[@id='4984880']/div/table/tbody/tr")
        #if (self.nowpage_146== 1) & ('1651779' in response.url) :
        #    self.totlepage_146 = int(
       #     response.xpath("//span[@class='default_pgTotalPage']/text()").extract()[0].encode(self.newEndcode))
        #if (self.nowpage_149== 1 )& ('1651780' in response.url ):
         #   self.totlepage_149 = int(
       #     response.xpath("//span[@class='default_pgTotalPage']/text()").extract()[0].encode(self.newEndcode))
        newbase_url = response.url
        nowItem = 0
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./td/div[2]/a/@href").extract()[0].encode(self.newEndcode), self.newEndcode)
            item["id"] = href.split('_')[2].split('.')[0]
            item["districtName"] = "杭州市"
            # print(href)

            url = self.base_url + href.replace("'", "")
            #print(url)
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
            item["noticePubDate"] = str(node.xpath("./td[@class='bt_time']/text()").extract()[0].encode(self.newEndcode),
                                        'utf-8').replace('[', '').replace(']', '')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "杭州财政"
            item["title"] = str(node.xpath("./td/div[2]/a/@title").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            if '1651779' in newbase_url:
                item["typeName"] = "招标公告"
            else:
                item["typeName"] = "中标公告"
            typename = item["typeName"]
            item["url"] = url
            page_now = int(response.url.split('&')[1].split('=')[1])
            if (page_now == 1 )and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=[ '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '杭州财政',
                           cont='<h1>今日爬取地址{}\r\n<br>杭州财政网站最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1
            yield item

        if response.xpath("//a[@class='default_pgBtn default_pgNext']/@href"):
            page = int(response.url.split('&')[1].split('=')[1])
            logging.info(typename + "现在爬取第{}页内容".format(page + 1))
            # print(str(self.nowpage)+'-----'+response.url)
            page += 1
            newurl = newbase_url[:newbase_url.index('&') + 1] + 'pageNum=' + str(page)
            # print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//td[@class='bt_content']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//td[@class='bt_content']//*/text()").extract()).encode(self.newEndcode), 'utf-8')
        item["keywords"] = str(''.join(response.xpath("//td[@class='bt_content']//*/text()").extract()).encode(self.newEndcode),
                               'utf-8')[:100]
        item["noticeTitle"] = str(
            response.xpath("//td[@class='title']/text()").extract_first().encode(self.newEndcode), 'utf-8')
        # print(item)
        yield item


if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_hz".split())

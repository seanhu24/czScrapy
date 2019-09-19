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
class AppSySpider(scrapy.Spider):
    name = 'app_sy'
    allowed_domains = ['ztb.shangyu.gov.cn']
    start_urls = ['http://ztb.shangyu.gov.cn/col/col1513290/index.html?uid=4687433&pageNum=1', 'http://ztb.shangyu.gov.cn/col/col1513303/index.html?uid=4687433&pageNum=1' , 'http://ztb.shangyu.gov.cn/col/col1513311/index.html?uid=4687433&pageNum=1' , 'http://ztb.shangyu.gov.cn/col/col1513286/index.html?uid=4687433&pageNum=1', 'http://ztb.shangyu.gov.cn/col/col1513307/index.html?uid=4687433&pageNum=1']
    base_url = 'http://ztb.shangyu.gov.cn'
    logging.info("开始爬取绍兴上虞----")

    newEndcode = "utf-8"
    if 'Linux' in platform.system() :
        chromeName ='chromedriver'
    else :
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
        logging.info("结束绍兴上虞的爬取---")
        self.browser.quit()

    def parse(self, response):
        #print(response.text)
        node_list = response.xpath("//div[@id='4687433']/div[@class='default_pgContainer']/ul/li")

        newbase_url = response.url
        nowItem = 0
        typename = ''
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./a/@href").extract()[0].encode(self.newEndcode), self.newEndcode)
            print(href)
            item["id"] = href.split('_')[2].split('.')[0]
            item["districtName"] = "上虞区"


            url = self.base_url + href.replace("'", "")
            #print(url)
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
            item["noticePubDate"] = str(node.xpath("./span/text()").extract()[0].encode(self.newEndcode),
                                        'utf-8').strip()
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "绍兴上虞区"
            item["title"] = str(node.xpath("./a/@title").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            if '1513290' in newbase_url:
                item["typeName"] = "招标产权交易"
            elif '1513303' in newbase_url:
                item["typeName"] = "中标产权交易"
            elif '1513311' in newbase_url:
                item["typeName"] = "成交产权交易"
            elif '1513286' in newbase_url:
                item["typeName"] = "招标国有产权交易"
            else:
                item["typeName"] = "成交国有产权交易"
            typename = item["typeName"]
            item["url"] = url
            page_now = int(response.url.split('&')[1].split('=')[1])
            if (page_now == 1)and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=['huxiao_hz@citicbank.com', '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '绍兴上虞区',
                           cont='<h1>今日爬取地址{}\r\n<br>绍兴上虞区最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1

            yield item


        if response.xpath("//a[@class='default_pgBtn default_pgNext']/@href"):
            page = int(response.url.split('&')[1].split('=')[1])
            logging.info(typename+"现在爬取第{}页内容".format(page + 1))
            #print(str(self.nowpage)+'-----'+response.url)
            page += 1
            newurl = newbase_url[:newbase_url.index('&') + 1] + 'pageNum=' + str(page)
            # print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)


    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
            ''.join(response.xpath("//div[@id='zoom']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@id='zoom']//*/text()").extract()).encode(self.newEndcode), 'utf-8').strip()
        item["keywords"] = str(''.join(response.xpath("//div[@id='zoom']//*/text()").extract()).encode(self.newEndcode),
                               'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            response.xpath("//div[@class='art_title']/h2/text()").extract_first().encode(self.newEndcode), 'utf-8').strip()
        # print(item)
        yield item


if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_sy".split())

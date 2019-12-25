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
class AppZjSpider(scrapy.Spider):
    name = 'app_zj'
    allowed_domains = ['zhuji.gov.cn']
    #start_urls = ['http://www.zhuji.gov.cn/col/col1679845/index.html?uid=5057605&pageNum=1','http://www.zhuji.gov.cn/col/col1679846/index.html?uid=5057613&pageNum=1']
    start_urls = ['http://www.zhuji.gov.cn/col/col1679846/index.html?uid=5057613&pageNum=1']
    base_url = 'http://www.zhuji.gov.cn'
    logging.info("开始爬取绍兴诸暨----")

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
        logging.info("结束绍兴诸暨的爬取---")
        self.browser.quit()

    def parse(self, response):
        print(response.text)
        newid = response.url.split('=')[1].split('&')[0]
        #print(newid)
        node_list = response.xpath("//div[@id='"+newid+"']/div[@class='default_pgContainer']/table/tbody/tr")

        newbase_url = response.url
        nowItem = 0
        typename = ''
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./td/a/@href").extract()[0].encode(self.newEndcode), self.newEndcode)
            #print(href)
            item["id"] = href.split('_')[2].split('.')[0]
            item["districtName"] = "诸暨市"


            url = self.base_url + href.replace("'", "")
            #print(url)

            item["noticePubDate"] = str(node.xpath("./td[2]/text()").extract()[0].encode(self.newEndcode),
                                        'utf-8').strip()
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "绍兴诸暨市"
            item["title"] = str(node.xpath("./td/a/@title").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            if '1679845' in newbase_url:
                item["typeName"] = "采购公告"
            else:
                item["typeName"] = "成交公告"
            typename = item["typeName"]
            item["url"] = url
            page_now = int(response.url.split('&')[1].split('=')[1])
            if (page_now == 1)and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=[ '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '绍兴诸暨市',
                           cont='<h1>今日爬取地址{}\r\n<br>绍兴诸暨最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1

            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)


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
            ''.join(response.xpath("//div[@class='main-fl bt-left']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@class='main-fl bt-left']//*/text()").extract()).encode(self.newEndcode), 'utf-8').strip()
        item["keywords"] = str(''.join(response.xpath("//div[@class='main-fl bt-left']//*/text()").extract()).encode(self.newEndcode),
                               'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            ''.join(response.xpath("//div[@class='main-fl-tit']/text()").extract()).encode(self.newEndcode), 'utf-8').strip()
        # print(item)
        yield item


if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_zj".split())

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
class AppZsSpider(scrapy.Spider):
    name = 'app_zs'
    allowed_domains = ['zscz.zhoushan.gov.cn']
    start_urls = ['http://zscz.zhoushan.gov.cn/col/col1561134/index.html?uid=4771635&pageNum=1']
    base_url = 'http://zscz.zhoushan.gov.cn'
    logging.info("开始爬取舟山----")

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
        logging.info("结束舟山的爬取---")
        self.browser.quit()

    def parse(self, response):
        #print(response.text)
        node_list = response.xpath("//div[@id='4771635']/div[@class='default_pgContainer']/ul/li[position()<last()]")

        newbase_url = response.url
        nowItem = 0
        typename = ''
        print(node_list)
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./h1/a/@href").extract()[0].encode(self.newEndcode), self.newEndcode)
            print(href)
            item["id"] = href.split('_')[2].split('.')[0]
            item["districtName"] = "舟山市"


            url = self.base_url + href.replace("'", "")
            #print(url)

            item["noticePubDate"] = str(node.xpath("./h3/text()").extract()[0].encode(self.newEndcode),
                                        'utf-8').strip().replace("(", "").replace(")", "")
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "舟山市"
            #item["title"] = str(node.xpath("./a/text()").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            item["typeName"] = "公告通知"
            typename = item["typeName"]
            item["url"] = url
            page_now = int(response.url.split('&')[1].split('=')[1])
            if (page_now == 1)and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=[ '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '舟山市',
                           cont='<h1>今日爬取地址{}\r\n<br>舟山市最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1

            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)


        if  response.xpath("//a[@class='default_pgBtn default_pgNext']/@href"):
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
            ''.join(response.xpath("//div[@class='class_listright']").extract()).encode(self.newEndcode),
            'utf-8')
        item["noticeContent"] = str(
            ''.join(response.xpath("//div[@class='class_listright']//*/text()").extract()).encode(self.newEndcode), 'utf-8').strip()
        item["keywords"] = str(''.join(response.xpath("//div[@class='class_listright']//*/text()").extract()).encode(self.newEndcode),
                               'utf-8').strip()[:100]
        item["noticeTitle"] = str(
            response.xpath("//div[@class='clshow_tit']/text()").extract_first().encode(self.newEndcode), 'utf-8').strip().replace("\n",'').replace(" ","")
        # print(item)
        item["title"] = item["noticeTitle"]
        yield item


if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_zs".split())

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
#无头浏览器设置
chorme_options = Options()
chorme_options.add_argument("--headless")
chorme_options.add_argument("--disable-gpu")
chorme_options.add_argument('--no-sandbox')
# prefs = {'profile.managed_default_content_settings.images': 2}
# options.add_experimental_option('prefs', prefs)
chorme_options.add_argument('--disable-java')
chorme_options.add_argument('--blink-settings=imagesEnabled=false')

class AppYcSpider(scrapy.Spider):
    name = 'app_yc'
    allowed_domains = ['sxyc.gov.cn']
    #start_urls = ['http://www.sxyc.gov.cn/col/col1559789/index.html?uid=4851098&pageNum=2','http://www.sxyc.gov.cn/module/jpage/dataproxy.jsp?page=1&appid=1&appid=1&webid=3090&path=/&columnid=1559789&unitid=4851098&webname=%E7%BB%8D%E5%85%B4%E5%B8%82%E8%B6%8A%E5%9F%8E%E5%8C%BA%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C%EF%BC%88%E9%AB%98%E6%96%B0%E5%8C%BA%E3%80%81%E8%A2%8D%E6%B1%9F%E5%BC%80%E5%8F%91%E5%8C%BA%E7%AE%A1%E5%A7%94%E4%BC%9A%EF%BC%89&permissiontype=0']
    start_urls = ['http://www.sxyc.gov.cn/col/col1559789/index.html?uid=4851098&pageNum=1','http://www.sxyc.gov.cn/col/col1559790/index.html?uid=4851098&pageNum=1']
    base_url ='http://www.sxyc.gov.cn'
    logging.info("开始爬取绍兴市越城区人民政府（高新区、袍江开发区管委会）----")
    totlepage_89 =1
    nowpage_89 = 1
    totlepage_90 = 1
    nowpage_90 = 1
    newEndcode = "utf-8"
    local_path =os.path.abspath('chromedriver')
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #print(local_path)
    # 实例化一个浏览器对象
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chorme_options, executable_path=self.local_path)
        super().__init__()

    # 整个爬虫结束后关闭浏览器
    def close(self, spider):
        logging.info("结束绍兴市越城区人民政府（高新区、袍江开发区管委会）的爬取---")
        self.browser.quit()


    def parse(self, response):
        #print(response.text)
        node_list = response.xpath("//div[@id='4851098']/div/li")
        if (self.nowpage_89 == 1) & ('1559789' in response.url):
            self.totlepage_89 = int(
                response.xpath("//span[@class='default_pgTotalPage']/text()").extract()[0].encode(self.newEndcode))
        if (self.nowpage_90 == 1) & ('1559790' in response.url):
            self.totlepage_90 = int(
                response.xpath("//span[@class='default_pgTotalPage']/text()").extract()[0].encode(self.newEndcode))
        #self.totlepage = int(response.xpath("//span[@class='default_pgTotalPage']/text()").extract()[0].encode(self.newEndcode))
        newbase_url = response.url
        nowItem = 0
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./a/@href").extract()[0].encode(self.newEndcode),self.newEndcode)
            item["id"] = href.split('_')[2].split('.')[0]
            item["districtName"] = "越城区"
            #print(href)

            url = self.base_url + href.replace("'" , "")
            print(url)
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
            item["noticePubDate"] = str(node.xpath("./span/text()").extract()[0].encode(self.newEndcode), 'utf-8').replace('[', '').replace(']', '')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "绍兴市越城区人民政府（高新区、袍江开发区管委会）"
            item["title"] = str(node.xpath("./a/@title").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            if '1559789' in newbase_url:
                item["typeName"] = "招标公告"
            else :
                item["typeName"] = "中标公示"
            item["url"] = url
            if (self.nowpage_89 == 1 | self.nowpage_90 == 1) and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=[ '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '绍兴越城招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>杭州绍兴越城网站最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1
            yield item

        if (self.nowpage_89 < self.totlepage_89) & ('1559789' in response.url):
            logging.info("招标公告现在爬取第{}页内容".format(self.nowpage_89 +1))
            self.nowpage_89 += 1
            newurl = newbase_url[:newbase_url.index('&')+1] + 'pageNum=' + str(self.nowpage_89)
            #print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)
        if (self.nowpage_90 < self.totlepage_90) & ('1559790' in response.url):
            logging.info("中标公示现在爬取第{}页内容".format(self.nowpage_90 +1))
            self.nowpage_90 += 1
            newurl = newbase_url[:newbase_url.index('&')+1] + 'pageNum=' + str(self.nowpage_90)
            #print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)
    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
                ''.join(response.xpath("//div[@id='zoom']").extract()).encode(self.newEndcode),
                'utf-8')
        item["noticeContent"] = str(''.join(response.xpath("//div[@id='zoom']//*/text()").extract()).encode(self.newEndcode), 'utf-8')
        item["keywords"] = str(''.join(response.xpath("//div[@id='zoom']//*/text()").extract()).encode(self.newEndcode), 'utf-8')[:100]
        item["noticeTitle"] = str(
            ''.join(response.xpath("//div[@class='con']/p[@class='con-title']/text()").extract()).encode(self.newEndcode), 'utf-8')
        #print(item)
        yield item



if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_yc".split())
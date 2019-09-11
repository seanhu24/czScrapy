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

class AppYhSpider(scrapy.Spider):
    name = 'app_yh'
    allowed_domains = ['yuhang.gov.cn']
    start_urls = ['http://www.yuhang.gov.cn/col/col1532234/index.html?uid=4793621&pageNum=1','http://www.yuhang.gov.cn/col/col1532235/index.html?uid=4793621&pageNum=1']
    base_url ='http://www.yuhang.gov.cn'
    logging.info("开始爬取杭州市余杭区人民政府----")
    totlepage_1532234 =1
    nowpage_1532234 = 1
    totlepage_1532235 = 1
    nowpage_1532235 = 1
    newEndcode = "utf-8"
    local_path =os.path.abspath('chromedriver')
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(local_path)
    # 实例化一个浏览器对象
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chorme_options, executable_path=self.local_path)
        super().__init__()

    # 整个爬虫结束后关闭浏览器
    def close(self, spider):
        logging.info("结束杭州市余杭区人民政府的爬取---")
        self.browser.quit()


    def parse(self, response):
        #print(response.text)
        node_list = response.xpath("//div[@id='4793621']/div/li")
        if (self.nowpage_1532234 == 1) & ('1532234' in response.url):
            self.totlepage_1532234 = int(
                response.xpath("//span[@class='default_pgTotalPage']/text()").extract()[0].encode(self.newEndcode))
        if (self.nowpage_1532235 == 1) & ('1532235' in response.url):
            self.totlepage_1532235 = int(
                response.xpath("//span[@class='default_pgTotalPage']/text()").extract()[0].encode(self.newEndcode))
        #self.totlepage = int(response.xpath("//span[@class='default_pgTotalPage']/text()").extract()[0].encode(self.newEndcode))
        newbase_url = response.url
        nowItem = 0
        for node in node_list:
            item = czScrapyItem()
            href = str(node.xpath("./a/@href").extract()[0].encode(self.newEndcode),self.newEndcode)
            item["id"] = href.split('_')[2].split('.')[0]
            item["districtName"] = "余杭区"
            #print(href)

            url = self.base_url + href.replace("'" , "")
            #print(url)
            yield scrapy.Request(url, meta={'item': item}, callback=self.newparse)
            item["noticePubDate"] = str(node.xpath("./a/i/text()").extract()[0].encode(self.newEndcode), 'utf-8').replace('[', '').replace(']', '')
            # item["noticeTitle"] = self.new_item["noticeTitle"]
            self.newday = item["noticePubDate"]
            item["source"] = "杭州市余杭区人民政府"
            item["title"] = str(node.xpath("./a/span/text()").extract()[0].encode(self.newEndcode), 'utf-8')
            # print(node.xpath("./td[2]/a[2]/text()").extract()[0].encode(self.newEndcode).decode('utf-8'))
            if '1532234' in newbase_url:
                item["typeName"] = "招标公告"
            else :
                item["typeName"] = "中标公示"
            item["url"] = url
            if (self.nowpage_1532234 == 1 | self.nowpage_1532235 == 1) and nowItem == 0:
                logging.info("发送email-------")
                send_email(receiver=['huxiao_hz@citicbank.com', '16396355@qq.com', '8206741@163.com'],
                           # send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '杭州余杭招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>杭州余杭招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n", self.newday))
            nowItem += 1
            yield item

        if (self.nowpage_1532234 < self.totlepage_1532234) & ('1532234' in newbase_url):
            logging.info("招标公示现在爬取第{}页内容".format(self.nowpage_1532234 +1))
            self.nowpage_1532234 += 1
            newurl = newbase_url[:newbase_url.index('&')+1] + 'pageNum=' + str(self.nowpage_1532234)
            #print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)
        if (self.nowpage_1532235 < self.totlepage_1532235) & ('1532235' in newbase_url):
            logging.info("中标公示现在爬取第{}页内容".format(self.nowpage_1532235 +1))
            self.nowpage_1532235 += 1
            newurl = newbase_url[:newbase_url.index('&')+1] + 'pageNum=' + str(self.nowpage_1532235)
            #print(newurl)
            yield scrapy.Request(newurl, callback=self.parse)

    def newparse(self, response):
        # print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(
                ''.join(response.xpath("//div[@class='article-content']").extract()).encode(self.newEndcode),
                'utf-8')
        item["noticeContent"] = str(''.join(response.xpath("//div[@class='article-content']//*/text()").extract()).encode(self.newEndcode), 'utf-8')
        item["keywords"] = str(''.join(response.xpath("//div[@class='article-content']//*/text()").extract()).encode(self.newEndcode), 'utf-8')[:100]
        item["noticeTitle"] = str(
            response.xpath("//div[@class='article-title']/h3/text()").extract_first().encode(self.newEndcode), 'utf-8')
        #print(item)
        yield item



if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_yh".split())
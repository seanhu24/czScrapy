# -*- coding: utf-8 -*-
import scrapy
from czScrapy.items import czScrapyItem
import logging
import time
import uuid
import json
from scrapy import cmdline
from czScrapy.mail_utils import *
from scrapy.selector import Selector

class AppFySpider(scrapy.Spider):
    name = 'app_fy'
    allowed_domains = ['fuyang.gov.cn','zjzfcg.gov.cn']
    #start_urls = ['http://www.fuyang.gov.cn/col/col1416545/index.html']
    nowpage = 1
    totlepage = 1
    newEndcode = "utf-8"
    newday = ""
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logging.info("----开始爬取杭州富阳政府门户网站-------")
    def start_requests(self):
        headers = {
            'Cookie': 'acw_tc = 784e2c9415668935815022229e4756c7bb23a8158617ac49b5f06668370fa6;SERVERID = e146d554a29ee4143047c903abfbc3da | 1566976932 | 1566976712'
        }
        logging.info("现在爬取第{}页内容".format(self.nowpage))
        yield scrapy.FormRequest(
            url='http://www.fuyang.gov.cn//module/xxgk/search.jsp?area=&infotypeId=H001&vc_title=&vc_number=&vc_filenumber=',
            headers=headers,
            formdata={
                # 'infotypeId': '0',  # 这里不能给bool类型的True，requests模块中可以
                'fbtime': '',  # 这里不能给int类型的1，requests模块中可以
                'vc_all': '',
                'vc_filenumber': '',
                'vc_number': '',
                'currpage': str(self.nowpage),
                'vc_title': '',
                'sortfield': ", compaltedate: 0",
                'jdid': '2754',
                'divid': 'div1416545',
                'area': '',
                'infotypeId': 'H001',
                'texttype': '',
                'sortfield': ',compaltedate:0'
            },  # 这里的formdata相当于requ模块中的data，key和value只能是键值对形式
            callback=self.parse
        )



    def parse(self, response):
        #print(response.text)
        node_list = response.xpath("//ul[@class='content_right_ul']/li[@class='tab_box']")
        #print(response.xpath("//table[@class='tb_title']/*/tr/td[2]/a[last()]/text()"))
        self.totlepage = int(response.xpath("//table[@class='tb_title']/*/tr/td[2]/a[last()]/text()").extract()[0].encode(self.newEndcode))
        nowitem = 0
        for node in node_list :
            item = czScrapyItem()
            href = str(node.xpath("./a/@href").extract()[0].encode("utf-8"), 'utf-8')
            #print(href)
            #print(href.split('_'))
            if 'fuyang'  in href :
                item["id"] = href.split('_')[2].split('.')[0]
                yield scrapy.Request(href, meta={'item': item}, callback=self.newparse)
                #continue
            elif 'zjzfcg' in href :
                item["id"] = href[href.index('=')+1:]
                url ='http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?noticeId={}&url=http%3A%2F%2Fnotice.zcygov.cn%2Fnew%2FnoticeDetail'.format(item["id"])
                yield scrapy.Request(url, meta={'item': item}, callback=self.newparse_zf)
            else:
                continue
            item["districtName"] = "富阳区"

            item["noticePubDate"] = str(node.xpath("./a/span[2]/text()").extract()[0].encode(self.newEndcode), 'utf-8')
            item["source"] = "杭州市富阳区人民政府门户网站"
            item["title"] = str(node.xpath("./a/span/span/@mc").extract()[0].encode(self.newEndcode), 'utf-8')
            item["typeName"] = "公告公示"
            item["url"] = href
            self.newday = item["noticePubDate"]

            if self.nowpage == 1 and nowitem== 0:
                logging.info("发送email-------")
                # send_email(receiver=['huxiao_hz@citicbank.com', '16396355@qq.com', '8206741@163.com'],
                send_email(receiver=['8206741@163.com'],
                           title=self.curr_time + '杭州市富阳区招标网站',
                           cont='<h1>今日爬取地址{}\r\n<br>杭州富阳区招标网站最新更新日期是{}</h1>'.format(response.url + "\r\n",
                                                                                      self.newday))
            nowitem += 1
            #print(item)
            yield item
        if self.nowpage<= self.totlepage:
            self.nowpage+=1
            headers = {
                'Cookie': 'acw_tc = 784e2c9415668935815022229e4756c7bb23a8158617ac49b5f06668370fa6;SERVERID = e146d554a29ee4143047c903abfbc3da | 1566976932 | 1566976712'
            }
            logging.info("现在爬取第{}页内容".format(self.nowpage))
            yield scrapy.FormRequest(
                url='http://www.fuyang.gov.cn//module/xxgk/search.jsp?area=&infotypeId=H001&vc_title=&vc_number=&vc_filenumber=',
                headers=headers,
                formdata={
                    # 'infotypeId': '0',  # 这里不能给bool类型的True，requests模块中可以
                    'fbtime': '',  # 这里不能给int类型的1，requests模块中可以
                    'vc_all': '',
                    'vc_filenumber': '',
                    'vc_number': '',
                    'currpage': str(self.nowpage),
                    'vc_title': '',
                    'sortfield': ", compaltedate: 0",
                    'jdid': '2754',
                    'divid': 'div1416545',
                    'area': '',
                    'infotypeId': 'H001',
                    'texttype': '',
                    'sortfield': ',compaltedate:0'
                },  # 这里的formdata相当于requ模块中的data，key和value只能是键值对形式
                callback=self.parse
            )

    def newparse(self, response):
        #print(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = str(''.join(response.xpath("//div[@class ='details-content']//*").extract()).encode(self.newEndcode), 'utf-8')
        item["noticeContent"] = str(''.join(response.xpath("//div[@class ='details-content']//*/text()").extract()).encode(self.newEndcode), 'utf-8')
        item["keywords"] = str(''.join(response.xpath("//div[@class ='details-content']//*/text()").extract()).encode(self.newEndcode), 'utf-8')[:100]
        item["noticeTitle"] = str(''.join(response.xpath("//div[@class='title']/text()").extract()).strip().encode(self.newEndcode), 'utf-8')
        #print(item)
        yield item
    def newparse_zf(self , response):
        #print(response.text)
        res = json.loads(response.text)
        # 接收上级已爬取的数据
        item = response.meta['item']
        item["noticeContent_html"] = res.get("noticeContent")
        item["noticeContent"] = str(''.join(''.join(Selector(text=res.get("noticeContent")).xpath("string(//div)").extract()).split()).encode(self.newEndcode),'utf-8')
        item["keywords"] = str(''.join(''.join(Selector(text=res.get("noticeContent")).xpath("string(//div)").extract()).split()).encode(self.newEndcode),'utf-8')[:100]
        item["noticeTitle"] = res.get("noticeTitle")
        #print(item)
        yield item
if __name__ == "__main__":
    cmdline.execute("scrapy crawl app_fy".split())
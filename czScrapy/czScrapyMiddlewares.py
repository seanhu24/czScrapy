# -- coding: utf-8 --
from scrapy.http import HtmlResponse
import time
from czScrapy.config import *
class czScrapyMiddlewares(object):

    # 可以拦截到request请求
    def process_request(self, request, spider):
        # 在进行url访问之前可以进行的操作, 更换UA请求头, 使用其他代理等
        pass

    # 可以拦截到response响应对象(拦截下载器传递给Spider的响应对象)
    def process_response(self, request, response, spider):
        """
                      三个参数:
                      # request: 响应对象所对应的请求对象
                      # response: 拦截到的响应对象
                      # spider: 爬虫文件中对应的爬虫类 WangyiSpider 的实例对象, 可以通过这个参数拿到 WangyiSpider 中的一些属性或方法
                      """

        #  对页面响应体数据的篡改, 如果是每个模块的 url 请求, 则处理完数据并进行封装
        referer = request.url
        if referer:
            request.headers["referer"] = referer
        flag = False
        for i in range(len(CONFIG_SITE)) :
           if CONFIG_SITE[i] in request.url :
            flag =True

        if flag:
            spider.browser.get(url=request.url)
            #more_btn = spider.browser.find_element_by_class_name("default_pgBtn default_pgNext")     # 更多按钮
            # print(more_btn)
            js = "window.scrollTo(0,document.body.scrollHeight)"
            spider.browser.execute_script(js)
            # if more_btn and request.url == "http://news.163.com/domestic/":

            time.sleep(1)  # 等待加载,  可以用显示等待来优化.
            #more_btn.click()
            row_response = spider.browser.page_source
            return HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8",
                                request=request)  # 参数url指当前浏览器访问的url(通过current_url方法获取), 在这里参数url也可以用request.url
            # 参数body指要封装成符合HTTP协议的源数据, 后两个参数可有可无
        else:
            return response

    # 请求出错了的操作, 比如ip被封了,可以在这里设置ip代理
    def process_exception(self, request, exception, spider):
        print("出现错误")

import scrapy
import sys
from scrapy.selector import HtmlXPathSelector
reload(sys)

'''
天山网维语板块爬虫

从link.txt中读取对应连接进行爬虫
爬虫内容保存在content.txt

'''

class TianShanContentSpider(scrapy.Spider):
    sys.setdefaultencoding("utf-8")
    name = "content"
    allowed_domain = ["uy.ts.cn"]
    content_file = 'content.txt'
    f_content = open(content_file, 'ab')

    link_file = 'link.txt'
    f_link = open(link_file)

    start_urls = []

    for line in f_link.readlines():
        line = line.strip()
        start_urls.append(line)

    def parse(self, response):
        self.content_parser(response)

    def content_parser(self, response):
        selector = HtmlXPathSelector(response)
        contents = selector.select(
            "//div[@id='content']/div[@class='right']/div[@class='content']/div[@id='content_value']/p/font/text()").extract()
        for content in contents:
            self.f_content.write(content)
            self.f_content.write('\r\n')

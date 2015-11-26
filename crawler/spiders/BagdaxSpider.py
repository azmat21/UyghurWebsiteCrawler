import scrapy
import sys
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from scrapy.http import Request
reload(sys)

'''
Bagdax论坛爬虫

爬虫内容保存在bagdax.txt

'''

class BagdaxSpider(scrapy.Spider):

    sys.setdefaultencoding("utf-8")

    file_name = "bagdax.txt"
    f_file = open(file_name, "w")

    name = "bagdax"
    allowed_domain = ["bbs.bagdax.cn"]
    start_urls = [
        "http://bbs.bagdax.cn/forum.php"
    ]

    # 获取子版块地址
    def parse(self, response):
        base_url = get_base_url(response)
        hxs = HtmlXPathSelector(response)
        links = hxs.xpath("//td/h2/a/@href").extract()
        for link in links:
            link = urljoin_rfc(base_url, link)
            yield Request(link, callback=self.parse_forum_list)

    # 获取每个板块的总页数并且请求每个页面
    def parse_forum_list(self, response):
        hxs = HtmlXPathSelector(response)
        last_page = hxs.xpath("//span[@id = 'fd_page_bottom']/div/label/span/@title").extract()
        page = last_page[0].split(' ')[1]
        # self.parse_list_by_page(response.url, page)
        dot = response.url.split('-')
        line = dot[2].split('.')
        for i in range(1, int(page)+1, 1):
            url = dot[0] + "-" + dot[1] + "-" + str(i) + "." + line[1]
            yield Request(url, callback=self.parse_list_content)

    # 获取每个列表地址
    def parse_list_content(self, response):
        base_url = get_base_url(response)
        hxs = HtmlXPathSelector(response)
        links = hxs.xpath("//th[@class = 'new']/a[@class = 'xst']/@href").extract()
        for link in links:
            link = urljoin_rfc(base_url, link)
            yield Request(link, callback=self.parse_content)

    # 获取内容
    def parse_content(self, response):
        hxs = HtmlXPathSelector(response)
        contents = hxs.xpath("//td[@class = 't_f']/text()").extract()
        for content in contents:
            content = content.strip()
            self.f_file.write(content)
            self.f_file.write("\r\n")
            #print(content)



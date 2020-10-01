import scrap
import sys
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from scrapy.http import Request
reload(sys)

'''
Bagdax新闻爬虫

爬虫内容保存在bagdax.txt

'''

class BagdaxNews(scrapy.Spider):

    sys.setdefaultencoding("utf-8")
    name = "bagdaxnews"
    start_urls = []
    file_name = "bagdaxnews.txt"
    f_file = open(file_name, 'w')

    # 板块地址及总页数
    urls = {
        "http://world.bagdax.cn/": '340',
        "http://cn.bagdax.cn/": '43',
        "http://xj.bagdax.cn/": '34',
        "http://finance.bagdax.cn/": '8',
        "http://special.bagdax.cn/": '1',
        "http://entrepreneur.bagdax.cn/": '2',
        "http://enterprise.bagdax.cn/": '3',
        "http://study-abroad.bagdax.cn/": '1',
        "http://wiki.bagdax.cn/": '1',
        "http://sports.bagdax.cn/": '19',
        "http://mixed.bagdax.cn/": '20'
    }

    for key, values in urls.items():
        start_urls.append(key)
        if values > 1:
            for i in range(2, int(values), 2):
                url = key + str(i) + ".html"
                start_urls.append(url)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath("//ul/li/font/a/@href").extract()
        for title in titles:
            print(title)
            yield Request(title, callback=self.parse_content)

    def parse_content(self, response):
        hxs = HtmlXPathSelector(response)
        contents = hxs.xpath("//div[@class = 'content_page']/p/text()").extract()
        for content in contents:
            self.f_file.write(content)
            self.f_file.write("\r\n")

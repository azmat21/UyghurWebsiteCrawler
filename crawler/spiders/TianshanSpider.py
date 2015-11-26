import scrapy
import sys
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
reload(sys)

'''

天山网维语板块爬虫

列表连接保存在link.txt
标题保存在title.txt

'''
class TianShanSpider(scrapy.Spider):

    sys.setdefaultencoding("utf-8")
    name = "tianshan"
    allowed_domain = ["uy.ts.cn"]
    link_file = 'link.txt'
    f_link = open(link_file, 'wb')

    title_file = "title.txt"
    f_title = open(title_file, 'wb')
    start_urls = []
    # "http://uy.ts.cn/homepage/content/2015-11/25/content_474974.htm"

    # 板块地址及总页数
    urls = {
        "http://uy.ts.cn/news/node_899": '100',  # xinjiang,
        "http://uy.ts.cn/news/node_900": '100',  # memliket
        "http://uy.ts.cn/news/node_901": '100',  # heliqara
        "http://uy.ts.cn/news/node_1075": '100',  # urumqi
        "http://uy.ts.cn/news/node_14742": '100',  # bir belbag
        "http://uy.ts.cn/node_964": '50',  # mohet 50
        "http://uy.ts.cn/news/node_904": '100',  # wilayet oblast hewerleri
        "http://uy.ts.cn/news/node_905": '100',  # pan maarip
        "http://uy.ts.cn/life/index": '98',  # turmush logeti 98
        "http://uy.ts.cn/wenxue/node_922": '45',  # adabe senet 45
        "http://uy.ts.cn/wenxue/node_926": '68',  # shier 68
        "http://uy.ts.cn/wenxue/node_924": '23',  # termilar 23
        "http://uy.ts.cn/xinjiang/node_913": '56',  # sayahet 56
        "http://uy.ts.cn/xinjiang/node_914": '15',  # seylighaf 15
        "http://uy.ts.cn/node_3641": '2',  # nizam 2,
        "http://uy.ts.cn/node_3343": '71',  # uchurlar 71
        "http://uy.ts.cn/node_3344": '40',  # sawatlar
    }

    # 根据地址和页数构造爬虫地址
    for key, value in urls.items():
        start_urls.append(key+".htm")
        for i in range(2, int(value), 1):
            url = key + "_" + str(i) + ".htm"
            start_urls.append(url)

    def parse(self, response):
        self.list_arse(response)

    def list_arse(self, response):
        base_url = get_base_url(response)
        selector = HtmlXPathSelector(response)
        titles = selector.select("//div[@class='layout']/div[@id='item_list']/a/em/text()").extract()
        for title in titles:
            print(title)
            self.f_title.write(title)
            self.f_title.write('\r\n')

        titles = selector.xpath("//div[@class='layout']/div[@id='item_list']/a/@href").extract()
        for title in titles:
            url = urljoin_rfc(base_url, title)
            print(url)
            self.f_link.write(url)
            self.f_link.write('\r\n')


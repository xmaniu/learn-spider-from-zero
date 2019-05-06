import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from zhuanti.items import ZhuantiItem

class zhuanti(CrawlSpider):
    name = 'zhuanti'
    start_urls = ['https://www.jianshu.com/recommendations/collections?page=1&order_by=hot']

    def parse(self, response):
        item = ZhuantiItem()
        selector = Selector(response)
        infos = selector.xpath('//div[@class="col-xs-8"]')
        #print(infos)
        for info in infos:
            print(info.extract())
            try:
                name = info.xpath('div/a/h4/text()').extract()[0]
                content = info.xpath('div/a/p/text()').extract()[0]
                article = info.xpath('div/div/a/text()').extract()[0]
                fans = info.xpath('div/div/text()').extract()[0]

                item['name'] = name
                item['content'] = content
                item['article'] = article
                item['fans'] = fans
                print(name,content,article,fans)
                yield item
            except IndexError:
                pass

        urls = ['https://www.jianshu.com/recommendations/collections?page={}&order_by=hot'.format(str(i)) for i in range(2,39)]
        for url in urls:
            yield Request(url,callback=self.parse)
import scrapy
from cnblog.items import CnblogItem


class CnblogSpiderSpider(scrapy.Spider):
    name = 'cnblog_spider_1'
    start_urls = ['https://www.cnblogs.com/']
    url = 'https://www.cnblogs.com/#p{}'
    page = 2

    def parse(self, response):
        article_list = response.xpath('//*[@id="post_list"]/article')
        item = CnblogItem()
        for artilce in article_list:
            item['title'] = artilce.xpath('.//div[@class="post-item-text"]/a/text()').extract_first()
            item['link'] = artilce.xpath('.//div[@class="post-item-text"]/a/@href').extract_first()
            yield item
        print('第' + str(self.page-1) + '页完成')

        if self.page <= self.settings.get('MAX_PAGE'):
            new_url = self.url.format(self.page)
            self.page += 1
            yield scrapy.Request(new_url, callback=self.parse, dont_filter=True)



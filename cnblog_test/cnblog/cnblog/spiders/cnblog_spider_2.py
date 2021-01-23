import scrapy
from cnblog.items import CnblogItem


class CnblogSpiderSpider(scrapy.Spider):
    name = 'cnblog_spider_2'
    start_urls = ['https://www.cnblogs.com/']

    def start_requests(self):
        start_url = 'https://www.cnblogs.com/#p{}'
        for page in range(1,201):
            url = start_url.format(page)
            yield scrapy.Request(url, self.parse, meta={'page': page}, dont_filter=True)



    def parse(self, response):
        article_list = response.xpath('//*[@id="post_list"]/article')
        item = CnblogItem()
        for artilce in article_list:
            item['title'] = artilce.xpath('.//div[@class="post-item-text"]/a/text()').extract_first()
            item['link'] = artilce.xpath('.//div[@class="post-item-text"]/a/@href').extract_first()
            yield item
        print('第' + str(response.meta.get('page')) + '页完成')




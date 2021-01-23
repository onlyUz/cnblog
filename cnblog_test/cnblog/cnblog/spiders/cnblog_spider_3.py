import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from cnblog.items import CnblogItem


class CnblogSpider2Spider(CrawlSpider):
    name = 'cnblog_spider_3'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.cnblogs.com/']
    page = 1

    rules = (
        Rule(LinkExtractor(allow=r'/sitehome/p/\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="paging_block"]/div/a[1]'), callback='parse_item', follow=False)
    )

    def parse_item(self, response):
        article_list = response.xpath('//*[@id="post_list"]/article')
        item = CnblogItem()
        for artilce in article_list:
            item['title'] = artilce.xpath('.//div[@class="post-item-text"]/a/text()').extract_first()
            item['link'] = artilce.xpath('.//div[@class="post-item-text"]/a/@href').extract_first()
            yield item
        # print('第' + str(self.page) + '页完成')
        # self.page += 1

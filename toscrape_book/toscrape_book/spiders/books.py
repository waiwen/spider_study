# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider
from toscrape_book.items import BookItem

class BooksSpider(RedisSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]

    # 2、将start_urls注释掉
    # start_urls = ['http://books.toscrape.com/']

     #书籍列表页面的解释数据
    def parse(self, response):
        #获取每本书的链接，发起request
        le = LinkExtractor(restrict_css="article.product_pod h3")
        for link in le.extract_links(response):
            yield scrapy.Request(link.url,callback=self.parse_book)
        #获取下一页的链接，发起request
        le = LinkExtractor(restrict_css="ul.pager li.next")
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url,callback=self.parse)

    #书籍页面的解释数据
    def parse_book(self,response):
        book = BookItem()
        sel = response.css('div.product_main')
        book['name'] = sel.xpath('./h1/text()').extract_first()
        book['price'] = sel.css('p.price_color::text').extract_first()
        book['review_rating'] = sel.css('p.star-rating::attr(class)').re_first('star-rating ([A-Za-z]+)')
        sel = response.css('table.table-striped')
        book['upc'] = sel.xpath('(.//tr)[1]/td/text()').extract_first()
        book['stock'] = sel.xpath('(.//tr)[last()-1]/td/text()').re_first('\((\d+) available\)')
        book['review_num'] = sel.xpath('(.//tr)[last()]/td/text()').extract_first()
        yield book






# -*- coding: utf-8 -*-
import scrapy


class ImagesSpider(scrapy.Spider):
    name = "images"
    allowed_domains = ["pixabay.com"]
    start_urls = ['http://pixabay.com/']

    def parse(self, response):
        pass

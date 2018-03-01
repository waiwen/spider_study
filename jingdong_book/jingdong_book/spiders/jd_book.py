# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest

lua_script = '''
function main(splash)
   splash:go(splash.arg.url)
   splash:wait(2)
   splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
   spalsh:wait(2)
   return splash:html()
end

'''


class JdBookSpider(scrapy.Spider):
    name = "jd_book"
    allowed_domains = ["search.jd.com"]
    start_urls = ['http://search.jd.com/']
     #搜索关键词
    KEY_WORDS = 'python'
    #请求url拼接
    BASE_URL = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&wq=%s'%(KEY_WORDS,KEY_WORDS)

    def start_requests(self):
        yield Request(self.BASE_URL,callback=self.parse_urls,dont_filter = True)


    def parse_urls(self,response):
        total = int(response.css('span#J_resCount::text').extract_first()[:-1])
        pageNum = total//60+(1 if total % 60 else 0)

        for i in range(pageNum):
            url = '%s&page=%s'%(self.BASE_URL,2*i+1)
            yield SplashRequest(url,
                                endpoint = 'execute',
                                args = {'lua_source':lua_script},
                                cache_args = ['lua_source'],
                                )
    def parse(self,response):
        for sel in response.css('ul.gl-warp.clearfix>li.gl-item'):
            yield {
                'name':sel.css('div.p-name').xpath('string(.//em)').extract_first(),
                'price':sel.css('div.p-price i::text').extract_first()
                        }





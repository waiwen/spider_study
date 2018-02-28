# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#将item输出前的处理钩子，parse函数后经过该钩子

class ToscrapeBookPipeline(object):
    review_rating_map = {
        'One':1,
        'Two':2,
        'Three':3,
        'Four':4,
        'Five':5
    }
    def process_item(self, item, spider):

        rating = item.get('review_rating')
        if rating:
            item['review_rating'] = self.review_rating_map[rating]
        item['stock'] = int(item['stock'])
        item['price'] = float(item['price'][2:])
        item['review_num'] = int(item['review_num'])
        return item

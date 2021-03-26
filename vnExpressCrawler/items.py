# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    articleID = scrapy.Field()
    sapo = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    displayContent = scrapy.Field()
    thumbnail = scrapy.Field()

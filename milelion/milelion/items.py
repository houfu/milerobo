# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MilelionArticle(scrapy.Item):
    summary = scrapy.Field()
    date_pub = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()

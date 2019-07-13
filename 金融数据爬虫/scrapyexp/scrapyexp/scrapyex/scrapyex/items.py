# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class ScrapyexItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # author_url = Field()
    # author_name = Field()
    # new_article = Field()
    # style = Field()
    # focus = Field()
    # fans = Field()
    # article_num = Field()
    # write_num = Field()
    # like = Field()
    # news_url = Field()
    # news_title = Field()
    # news_article = Field()
    entry_title = Field()
    entry_base_info = Field()
    entry_context = Field()
    pass

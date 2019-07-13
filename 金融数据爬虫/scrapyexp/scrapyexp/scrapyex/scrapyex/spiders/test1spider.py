
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapyex.items import ScrapyexItem
import re


class Test1(CrawlSpider):
    name = 'test1'
    start_urls = ['http://www.baike.com/wiki/%E8%90%A5%E8%BF%90%E7%8E%B0%E9%87%91%E6%B5%81']
    #start_urls = ['https://baike.so.com/search/?q=tag%3A%E9%87%91%E8%9E%8D']

    def parse(self, response):
        base = 'https://baike.so.com'
        selector = Selector(response)
        print(response,'\n','\n')
        # infos = selector.xpath('//a').re(reg_img)

        infos = selector.xpath('//div[@class="entry-header"]')

        print(infos,'\n','\n')

        entry_title = selector.xpath('//div[@id="baike-title"]/h1/span/text()').extract()[0]
        print(entry_title, '\n', '\n')

        entry_content = selector.xpath('//div[@id="js-card-content"]/p//text()').extract()
        print(entry_content,'\n','\n')
        entry_content_text = "".join(entry_content)
        print(entry_content_text,'\n','\n')

        entry_base_info = selector.xpath('//div[@id="basic-info"]/div/ul/li')
        print(entry_base_info, '\n', '\n')
        entry_base_info_key = entry_base_info.xpath('div/p[@class="cardlist-name"]//@title').extract()
        print(entry_base_info_key, '\n', '\n')
        entry_base_info_value = entry_base_info.xpath('div/p[@class="cardlist-value"]//@title').extract()
        print(entry_base_info_value, '\n', '\n')
        entry_base_info_dict = dict(zip(entry_base_info_key,entry_base_info_value))
        print(entry_base_info_dict,'\n','\n')

        entry_url = selector.xpath('//div[@id="js-card-content"]/p/a/@href').extract()
        print(entry_url)

        entry_url_new = [base + url for url in entry_url]
        print(entry_url_new)

        # yield Request(Request.url,
        #        meta={'entry_title':entry_title,'entry_base_info':entry_base_info_dict,'entry_context':entry_content_text},
        #                     callback=self.parse_item)

        item = ScrapyexItem()
        item['entry_title'] = entry_title
        item['entry_base_info'] = entry_base_info_dict
        item['entry_context'] = entry_content_text

        yield item

        for url in entry_url_new:
            print(url)
            yield Request(url,callback=self.parse)



        # for info in infos:
                # print(info,'\n')
                # entry_title = selector.xpath('div/dl/dd/h1/text()').extract()[0]
                # print(entry_title,'\n')

                # author_name = info.xpath('div/a/h4/text()').extract()[0]
                # print(author_name,'\n','\n')
                # author_url = base + info.xpath('div/a/@href').extract()[0].split('/')[-1]
                # print(author_url,'\n','\n')
                # article = info.xpath('div/div[@class="recent-update"]')[0]
                # new_article = article.xpath('string(.)').extract()[0].strip('\n').replace(' ', '').replace('\n', '')
                # yield Request(author_url, meta={'author_url':author_url, 'author_name': author_name, 'new_article': new_article},
                #               callback=self.parse_item)
                # yield Request(response,
                #        meta={},
                #                     callback=self.parse_item)
        # urls = {'https://www.jianshu.com/recommendations/users?page={}'.format(str(i)) for i in range(2, 10)}
        # for url in urls:
        #     yield Request(url, callback=self.parse)

    def parse_item(self, response):
        item = ScrapyexItem()
        item['entry_title'] = response.meta['entry_title']
        item['entry_base_info'] = response.meta['entry_base_info']
        item['entry_context'] = response.meta['entry_context']
        #item['entry_title'] = response.meta['entry_title']
        # item['author_name'] = response.meta['author_name']
        # item['new_article'] = response.meta['new_article']
        try:
            selector = Selector(response)
            # entry_title = selector.xpath('//div[@id="baike-title"]/h1/span/text()').extract()[0]
            # print(entry_title,'\n','\n')
        #     if selector.xpath('//span[@class="author_tag"]'):
        #         style = '签约作者'
        #     else :
        #         style = '普通作者'
        #     focus = selector.xpath('//div[@class="info"]/ul/li[1]/div/a/p/text()').extract()[0]
        #     fans = selector.xpath('//div[@class="info"]/ul/li[2]/div/a/p/text()').extract()[0]
        #     article_num = selector.xpath('//div[@class="info"]/ul/li[3]/div/a/p/text()').extract()[0]
        #     write_num = selector.xpath('//div[@class="info"]/ul/li[4]/div/p/text()').extract()[0]
        #     like = selector.xpath('//div[@class="info"]/ul/li[5]/div/p/text()').extract()[0]
        #     item['style'] = style
        #     item['focus'] = focus
        #     item['fans'] = fans
        #     item['article_num'] = article_num
        #     item['write_num'] = write_num
        #     item['like'] = like
        #     news_article = selector.xpath('//p/text()').extract()
        #     content = ' '.join(news_article)
        #     print(content)
        #     item['news_article'] = content
            yield item
        except IndexError:
            pass

class Test2(CrawlSpider):
    name = 'test2'
    start_urls = ['http://www.baike.com/wiki/%E5%9F%BA%E9%87%91&prd=button_doc_entry']

    def parse(self, response):
        base = 'https://www.baike.com/wiki/'
        selector = Selector(response)
        print(response, '\n', '\n')
        # infos = selector.xpath('//a').re(reg_img)

        infos = selector.xpath('//div[@class="entry-header"]')

        print(infos, '\n', '\n')

        entry_title = selector.xpath('//div[@class="content-h1"]/h1/text()').extract()[0]
        print(entry_title, '\n', '\n')

        entry_content = selector.xpath('//div[@id="anchor"]/p//text()').extract()
        print(entry_content, '\n', '\n')
        entry_content_text = "".join(entry_content)
        print(entry_content_text, '\n', '\n')

        entry_base_info = selector.xpath('//div[@class="module zoom"]/table/tr/td')
        print(entry_base_info, '\n', '\n')
        entry_base_info_key = entry_base_info.xpath('strong/text()').extract()
        entry_base_info_key = [key.split("：")[0] for key in entry_base_info_key]
        print(entry_base_info_key, '\n', '\n')
        entry_base_info_value = entry_base_info.xpath('span/text()').extract()
        print(entry_base_info_value, '\n', '\n')
        entry_base_info_dict = dict(zip(entry_base_info_key, entry_base_info_value))
        print(entry_base_info_dict, '\n', '\n')

        entry_new_title = selector.xpath('//div[@id="xgct"]/ul/li/a/@title').extract()
        print(entry_new_title)

        entry_url_new = [base + new_title for new_title in entry_new_title]
        print(entry_url_new)

        item = ScrapyexItem()
        item['entry_title'] = entry_title
        item['entry_base_info'] = entry_base_info_dict
        item['entry_context'] = entry_content_text

        yield item

        for url in entry_url_new:
            print(url)
            yield Request(url,callback=self.parse)

        # print( '\n', '\n')
        # base = 'http://finance.sina.com.cn/roll/'
        # selector = Selector(response)
        # print(response)
        # #infos = selector.xpath('//tr')
        # infos = selector.xpath('//a[@target="blank"]')
        # print(infos,'\n','\n')
        # for info in infos:
        #         news_url = info.xpath('a/@href')
                # author_name = info.xpath('div/a/h4/text()').extract()[0]
                # print(author_name,'\n','\n')
                # author_url = base + info.xpath('div/a/@href').extract()[0].split('/')[-1]
                # print(author_url,'\n','\n')
                # article = info.xpath('div/div[@class="recent-update"]')[0]
                # new_article = article.xpath('string(.)').extract()[0].strip('\n').replace(' ', '').replace('\n', '')
                # yield Request(author_url, meta={'author_url':author_url, 'author_name': author_name, 'new_article': new_article},
                #               callback=self.parse_item)
                # yield Request(author_url,
                #       meta={'author_url': author_url},
                #                     callback=self.parse_item)
        # urls = {'https://www.jianshu.com/recommendations/users?page={}'.format(str(i)) for i in range(2, 10)}
        # for url in urls:
        #     yield Request(url, callback=self.parse)

    def parse_item(self, response):
        item = ScrapyexItem()
        item['entry_title'] = response.meta['entry_title']
        item['entry_base_info'] = response.meta['entry_base_info']
        item['entry_context'] = response.meta['entry_context']
        # item['author_name'] = response.meta['author_name']
        # item['new_article'] = response.meta['new_article']
        try:
            selector = Selector(response)
        #     if selector.xpath('//span[@class="author_tag"]'):
        #         style = '签约作者'
        #     else :
        #         style = '普通作者'
        #     focus = selector.xpath('//div[@class="info"]/ul/li[1]/div/a/p/text()').extract()[0]
        #     fans = selector.xpath('//div[@class="info"]/ul/li[2]/div/a/p/text()').extract()[0]
        #     article_num = selector.xpath('//div[@class="info"]/ul/li[3]/div/a/p/text()').extract()[0]
        #     write_num = selector.xpath('//div[@class="info"]/ul/li[4]/div/p/text()').extract()[0]
        #     like = selector.xpath('//div[@class="info"]/ul/li[5]/div/p/text()').extract()[0]
        #     item['style'] = style
        #     item['focus'] = focus
        #     item['fans'] = fans
        #     item['article_num'] = article_num
        #     item['write_num'] = write_num
        #     item['like'] = like
            yield item
        except IndexError:
            pass
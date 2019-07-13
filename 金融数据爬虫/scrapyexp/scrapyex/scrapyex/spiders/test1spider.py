#coding=utf-8
#作者：李蕴琦
#个人爬取数据使用，未曾共享，故未写注释
# from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapyex.items import ScrapyexItem


class Test1(CrawlSpider):
    name = 'test1'
    start_urls = [
        'http://fund.eastmoney.com/fund.html#os_0;isall_1;ft_|;pt_1']
    item = ScrapyexItem()
    def parse(self, response):
        # base1 = 'http://fund.eastmoney.com/'
        base2 = 'http://fundf10.eastmoney.com/'
        selector = Selector(response)
        infos = selector.xpath('//div[@id="tableDiv"]/table/tbody/tr/td[@class="tol"]/nobr')
        for info in infos:
            # author_name = info.xpath('div/a/h4/text()').extract()[0]
            # author_url = base + info.xpath('div/a/@href').extract()[0].split('/')[-1]
            # article = info.xpath('div/div[@class="recent-update"]')[0]
            # new_article = article.xpath('string(.)').extract()[0].strip('\n').replace(' ', '').replace('\n', '')
            # news_url = base1 + info.xpath('a/@href').extract()[0].split('/')[-1]
            # fund_url = base2 + 'jbgk_' + info.xpath('a/@href').extract()[0].split('/')[-1]
            manager_url = base2 + 'jjjl_' + info.xpath('a/@href').extract()[0].split('/')[-1]
            #yield_url = base2 + 'jdzf_' + info.xpath('a/@href').extract()[0].split('/')[-1]
            #rate_url = base2 + 'jjpj_' + info.xpath('a/@href').extract()[0].split('/')[-1]
            # tsdata = base2 + 'tsdata_' + info.xpath('a/@href').extract()[0].split('/')[-1]
            # yield Request(news_url, callback=self.parse_item1)
            # yield Request(fund_url, callback=self.parse_item2)
            yield Request(manager_url, callback=self.parse_item3)
            # yield Request(yield_url, callback=self.parse_item4)
            #yield Request(rate_url, callback=self.parse_item5)
            # yield Request(tsdata, callback=self.parse_item6)
            # yield Request(news_url, callback=self.parse)
        # urls = {'https://www.jianshu.com/recommendations/users?page={}'.format(str(i)) for i in range(2, 10)}
        # for url in urls:
        #     yield Request(url, callback=self.parse)

    # def parse_item1(self, response):
    #
    #     # item['author_url'] = response.meta['author_url']
    #     # item['author_name'] = response.meta['author_name']
    #     # item['new_article'] = response.meta['new_article']
    #     try:
    #         selector = Selector(response)
    #         # if selector.xpath('//span[@class="author_tag"]'):
    #         #     style = '签约作者'
    #         # else :
    #         #     style = '普通作者'
    #         # title = selector.xpath('//div[@class="content-h1"]/h1/text()').extract()[0]
    #         fund_name_code = selector.xpath('//div[@class="fundDetail-tit"]//text()').extract()
    #         information = selector.xpath('//div[@class="infoOfFund"]/table/tr//text()').extract()
    #         IOPV = selector.xpath('//dl[@class="dataItem02"]/dd[@class="dataNums"]/span/text()').extract()[0]
    #         turnover_rate = selector.xpath('//div[@class = "poptableWrap jjhsl"]/table/tbody//text()').extract()[5]
    #
    #         str = ""
    #         for i in fund_name_code:
    #             str = str + i
    #         self.item['fund_name_code'] = str
    #         self.item['fund_manager'] = information[6]
    #         self.item['fund_scale'] = information[4]
    #         self.item['fund_type'] = information[1] + information[2]
    #         self.item['establishment_date'] = information[8]
    #         self.item['GP'] = information[11]
    #         self.item['IOPV'] = IOPV
    #         self.item['turnover_rate'] = turnover_rate
    #
    #         yield self.item
    #     except IndexError:
    #         pass
    #
    # def parse_item2(self, response):
    #     print("2")
    #     try:
    #         selector = Selector(response)
    #         information = selector.xpath('//div[@class="box"]/table//text()').extract()
    #         dish_in_estimating = selector.xpath(
    #             '//div[@class="col-right"]/p[@class="row row1"]/label/span[@id="fund_gsz"]/text()').extract()[0]
    #         transaction_status = selector.xpath('//div[@class="col-right"]/p[@class="row"]/label/span/text()').extract()
    #         zero_norm = selector.xpath('//div[@class="col-left"]/div/a//text()').extract()
    #         for i in zero_norm:
    #             print(i)
    #         self.item['full_name'] = information[1]
    #         self.item['share_scale'] = information[15]
    #         self.item['fund_trustee'] = information[20]
    #         self.item['dish_in_estimating'] = dish_in_estimating
    #         self.item['management_cost'] = information[26]
    #         self.item['subscription_fee'] = information[32]
    #         self.item['buy_charge'] = information[34] + information[35] + information[36]
    #         self.item['redemption_fee'] = information[38]
    #         self.item['subscription_status'] = transaction_status[0]
    #         self.item['redemption_status'] = transaction_status[2]
    #         self.item['zero_norm'] = zero_norm[1] + zero_norm[3] + " " + zero_norm[6] + zero_norm[8]
    #         yield self.item
    #     except IndexError:
    #         pass

    def parse_item3(self, response):
        try:
            selector = Selector(response)
            url = selector.xpath(
                '//div[@class="box"]/div/table[@class="w782 comm  jloff"]/tbody/tr[1]/td[3]//a/@href').extract()
            for i in url:
                yield Request(i, callback=self.parse_item7)
        except IndexError:
            pass

    # def parse_item4(self, response):
    #     try:
    #         selector = Selector(response)
    #         ranking = selector.xpath(
    #             '//div[@id="jdzftable"]/div[@class="jdzfnew"]/ul/li[@class="tlpm"]//text()').extract()[0]
    #         print("4")
    #         self.item['rankings'] = ranking
    #         yield self.item
    #     except IndexError:
    #         pass

    # def parse_item5(self, response):
    #     print("5")
    #     try:
    #         selector = Selector(response)
    #         ratings = selector.xpath(
    #             '//div[@class="box"]/div/table/tbody/tr//text()').extract()
    #         self.item['investment_rating'] = ratings[1]
    #         self.item['Shanghai_securities_rating_three'] = ratings[2]
    #         self.item['Shanghai_securities_rating_five'] = ratings[3]
    #         self.item['jianjinxin_rating'] = ratings[4]
    #         yield self.item
    #     except IndexError:
    #         pass

    # def parse_item6(self, response):
    #     print("6")
    #     try:
    #         selector = Selector(response)
    #         styles = selector.xpath(
    #             '//div[@class="fgcontentfr"]/table/tr//text()').extract()
    #         volatility = selector.xpath(
    #             '//div[@class="box"]/div/div/table/tr//text()').extract()
    #         self.item['fund_investment_style'] = styles[5] + " " + styles[6]
    #         self.item['volatility'] = volatility[10]
    #         self.item['sharpe_ratio'] = volatility[14]
    #         yield self.item
    #     except IndexError:
    #         pass

    def parse_item7(self, response):
        try:
            selector = Selector(response)
            name = selector.xpath(
                '//div[@class="content_in "]/h4/span/text()').extract()[0]
            time = selector.xpath(
                '//div[@class="right jd "]//text()').extract()[2]
            self.item['name'] = name
            self.item['time'] = time
            yield self.item
        except IndexError:
            pass
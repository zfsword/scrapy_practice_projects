# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from zhilianJob.items import ZhilianjobItem


class ZhilianSpider(Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    # start_urls = ['http://zhaopin.com/']

    baseUrl = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl={jl}&kw={kw}&sm={sm}&p={p}'
    jl = '北京'
    kw = 'python'
    sm = '0'
    p = '1'


    def start_requests(self):
        yield Request(self.baseUrl.format(jl=self.jl, kw=self.kw, sm=self.sm, p=self.p), callback=self.parse_index)

    def parse_index(self, response):
        for job_url in response.xpath('//td[@class="zwmc"]/div/a/@href').extract():
            yield Request(job_url, callback=self.detail_info)

        # 10页以后不是时间太久就是非相关职位了
        current = int(response.xpath('//div[@class="pagesDown"]/ul/li/a[@class="current"]/text()').extract_first())
        nextPage = response.xpath('//div[@class="pagesDown"]/ul/li/a[@class="next-page"]/@href').extract_first()
        if nextPage:
            if current < 10:
                yield Request(nextPage, callback=self.parse_index)

    def detail_info(self, response):

        item_loader = ItemLoader(item=ZhilianjobItem(), response=response)
        # item_loader.default_output_processor = TakeFirst()
        item_loader.add_xpath('jobName', '//div[@class="inner-left fl"]/h1/text()')
        item_loader.add_xpath('welfare', '//div[@class="welfare-tab-box"]/span/text()')
        item_loader.add_xpath('salary', '//div[@class="terminalpage-left"]/ul/li[1]/strong/text()', TakeFirst(), str.strip)
        # item_loader.add_xpath('workPlace', '//div[@class="terminalpage-left"]/ul/li[2]/strong/text()')
        item_loader.add_xpath('releaseTime', '//div[@class="terminalpage-left"]/ul/li[3]/strong/span/text()')
        item_loader.add_xpath('jobNature', '//div[@class="terminalpage-left"]/ul/li[4]/strong/text()')
        item_loader.add_xpath('experience', '//div[@class="terminalpage-left"]/ul/li[5]/strong/text()')
        item_loader.add_xpath('education', '//div[@class="terminalpage-left"]/ul/li[6]/strong/text()')
        item_loader.add_xpath('numOfHiring', '//div[@class="terminalpage-left"]/ul/li[7]/strong/text()')
        item_loader.add_xpath('jobCategory', '//div[@class="terminalpage-left"]/ul/li[8]/strong/a/text()')
        item_loader.add_xpath('jobDescribe', '//div[@class="tab-cont-box"]/div[1]/p/text()', Join(), str.strip)
        item_loader.add_xpath('workPlace', '//div[@class="tab-cont-box"]/div[1]/h2/text()', Join(), str.strip)

        item_loader.add_xpath('companyName', '//p[@class="company-name-t"]/a/text()', TakeFirst(), str.strip)
        item_loader.add_xpath('companySize', '//div[@class="company-box"]/ul/li[1]/strong/text()', TakeFirst(), str.strip)
        item_loader.add_xpath('companyType', '//div[@class="company-box"]/ul/li[2]/strong/text()', TakeFirst(), str.strip)
        item_loader.add_xpath('inderstry', '//div[@class="company-box"]/ul/li[3]/strong/a/text()', TakeFirst(), str.strip)
        item_loader.add_css('companyDescribe', '.terminalpage-left .terminalpage-main .tab-cont-box div:nth-child(2) p::text', Join(), str.strip)
        return item_loader.load_item()

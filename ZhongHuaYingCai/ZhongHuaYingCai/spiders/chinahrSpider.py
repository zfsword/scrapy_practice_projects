# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from ZhongHuaYingCai.items import ZhonghuayingcaiItem

class ChinahrspiderSpider(Spider):
    name = 'chinahrSpider'
    allowed_domains = ['chinahr.com']
    # start_urls = ['http://chinahr.com/']
    city = '34,398'
    keyword = 'python'
    url = "http://www.chinahr.com/sou/?city={city}&keyword={keyword}"

    def start_requests(self):
        yield Request(self.url.format(city=self.city, keyword=self.keyword), callback=self.parse_index)

    def parse_index(self, response):
        for each in response.css('.jobList .l1 .e1>a::attr(href)').extract():
            yield Request(each, callback=self.parse_detail)

        nextPage = response.css('.pageList a:last-child::attr(href)').extract_first()
        if nextPage:
            yield Request('http://www.chinahr.com/sou/'+nextPage, callback=self.parse_index)


    def parse_detail(self, response):
        itemLoader = ItemLoader(item=ZhonghuayingcaiItem(), response=response)
        itemLoader.add_css('jobName', '.job_name::text')
        itemLoader.add_css('salary', '.job_price::text')
        itemLoader.add_css('jobLocation', '.job_require .job_loc::text')
        itemLoader.add_css('jobType', '.job_require span:nth-of-type(3)::text')
        itemLoader.add_css('education', '.job_require span:nth-of-type(4)::text')
        itemLoader.add_css('experience', '.job_exp::text')
        itemLoader.add_css('jobTags', '.job_fit_tags ul li::text')
        itemLoader.add_css('jobDescribe', '.job_intro_info::text', Join(), str.strip)
        itemLoader.add_css('companyName', '.job-company h4>a::text')
        itemLoader.add_css('inderstry', '.job-company tbody tr:nth-of-type(2) td:nth-child(2)::text', Join(), str.strip)
        itemLoader.add_css('companySize', '.job-company tbody tr:nth-of-type(3) td:nth-child(2)::text')
        itemLoader.add_css('companyTpye', '.job-company tbody tr:nth-of-type(4) td:nth-child(2)::text')
        itemLoader.add_css('companyDescribe', '.company_service::text', Join(), str.strip)
        return itemLoader.load_item()

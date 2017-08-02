# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from liepin.items import LiepinItem


class LiepinSpider(Spider):
    name = 'liepinSpider'
    allowed_domains = ['liepin.com']
    # start_url = ['https://www.liepin.com']
    base_url = 'https://www.liepin.com/zhaopin/?industries=&dqs=010&salary=&jobKind=&pubTime=&compkind=&compscale=&industryType=&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=1&fromSearchBtn=2&headckid=be679dbdcc3051e2&searchType=1&key={key}'
    key = 'python'


    def start_requests(self):
        yield Request(self.base_url.format(key=self.key), callback=self.parse_search_list)

    def parse_search_list(self, response):
        job_urls = response.xpath('//div[@class="job-info"]/h3/a/@href').extract()
        for url in job_urls:
            yield Request(url, callback=self.detail_info)

        nextPage = response.xpath('//div[@class="pagerbar"]/a[@class="current"]/following-sibling::*[1]/@href').extract_first()
        if nextPage:
            yield Request(nextPage, callback=self.parse_search_list)

    def detail_info(self, response):
        item = ItemLoader(item=LiepinItem(), response=response)
        item.add_xpath('jobName', '//div[@class="title-info"]/h1/text()')
        item.add_xpath('salary', '//p[@class="job-item-title"]/text()', TakeFirst(), str.strip)
        item.add_xpath('education', '//div[@class="job-qualifications"]/span[1]/text()', TakeFirst())
        item.add_xpath('experience', '//div[@class="job-qualifications"]/span[2]/text()', TakeFirst())
        item.add_xpath('language', '//div[@class="job-qualifications"]/span[3]/text()', TakeFirst())
        item.add_xpath('age', '//div[@class="job-qualifications"]/span[4]/text()', TakeFirst())
        item.add_xpath('jobTags', '//div[@class="tag-list"]/span/text()')
        item.add_xpath('jobDescribe', '//div[@class="job-item main-message"]/div[@class="content content-word"]/text()', Join(), str.strip)
        item.add_xpath('companyName', '//div[@class="company-infor"]/h4/a[1]/text()', TakeFirst())
        item.add_xpath('inderstry', '//div[@class="company-infor"]/ul/li[1]/text()', TakeFirst(), str.strip)
        item.add_xpath('finance', '//div[@class="company-infor"]/ul/li[2]/text()', TakeFirst())
        item.add_xpath('companySize', '//div[@class="company-infor"]/ul/li[3]/text()', TakeFirst())
        item.add_xpath('companyType', '//div[@class="company-infor"]/ul/li[4]/text()', TakeFirst())
        item.add_xpath('address', '//div[@class="company-infor"]/p/text()', Join(), str.strip)
        return item.load_item()

        #  item = LiepinItem()
        #  item['jobName'] = response.xpath('//div[@class="title-info"]/h1/text()'),
        #  item['salary'] = response.xpath('//p[@class="job-item-title"]/text()').extract_first().strip(),
        #  item['education'] = response.xpath('//div[@class="job-qualifications"]/span[1]/text()').extract_first(),
        #  item['experience'] = response.xpath('//div[@class="job-qualifications"]/span[2]/text()').extract_first(),
        #  item['language'] = response.xpath('//div[@class="job-qualifications"]/span[3]/text()').extract_first(),
        #  item['age'] = response.xpath('//div[@class="job-qualifications"]/span[4]/text()').extract_first(),
        #  item['jobTags'] = response.xpath('//div[@class="tag-list"]/span/text()').extract(),
        #  item['jobDescribe'] = ''.join(response.xpath('//div[@class="job-item main-message"]/div[@class="content content-word"]/text()').extract()),
        #  item['companyName'] = response.xpath('//div[@class="company-infor"]/h4/a[1]/text()').extract_first(),
        #  item['inderstry'] = response.xpath('//div[@class="company-infor"]/ul/li[1]/text()').extract_first(),
        #  item['finance'] = response.xpath('//div[@class="company-infor"]/ul/li[2]/text()').extract_first(),
        #  item['CompanySize'] = response.xpath('//div[@class="company-infor"]/ul/li[3]/text()').extract_first(),
        #  item['CompanyType'] = response.xpath('//div[@class="company-infor"]/ul/li[4]/text()').extract_first(),
        #  item['address'] = ''.join(response.xpath('//div[@class="company-infor"]/p/text()').extract()).strip()
        #  return item



# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join
from w3lib.html import remove_tags


class DajiejobItem(Item):

    jid = Field(output_processor=TakeFirst())
    jobName = Field(output_processor=TakeFirst())
    salary = Field(output_processor=TakeFirst())
    recruit = Field(output_processor=TakeFirst())   # 招聘人数
    experience = Field(output_processor=TakeFirst())  # 工作经验
    jobTags = Field()  # 工作标签
    releaseTime = Field(output_processor=TakeFirst())  # 发布时间
    jobDescribe = Field(output_processor=Join())  # 工作描述
    workPlace = Field(output_processor=TakeFirst())

    companyName = Field(output_processor=TakeFirst())  # 公司名称
    companySize = Field(output_processor=TakeFirst())  # 企业规模
    inderstry = Field(output_processor=TakeFirst())  # 公司行业
    companyType = Field(output_processor=TakeFirst())  # 企业类型
    website = Field(output_processor=TakeFirst())   # 官方网站
    companyDescribe = Field(output_processor=Join())  # 公司描述
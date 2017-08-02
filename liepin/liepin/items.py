# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join


class LiepinItem(Item):
    jobName = Field(output_processor=TakeFirst())  # 职位名称
    salary = Field(output_processor=TakeFirst())  # 工资
    education = Field(output_processor=TakeFirst())  # 学历
    experience = Field(output_processor=TakeFirst())  # 工作经验
    language = Field(output_processor=TakeFirst())  # 语言能力
    age = Field(output_processor=TakeFirst())  # 年龄
    jobTags = Field()  # 工作标签
    jobDescribe = Field(output_processor=Join())  # 工作描述

    companyName = Field(output_processor=TakeFirst())  # 公司名称
    inderstry = Field(output_processor=TakeFirst())  # 公司行业
    finance = Field(output_processor=TakeFirst())  # 资金状况
    companySize = Field(output_processor=TakeFirst())  # 企业规模
    companyType = Field(output_processor=TakeFirst())  # 企业类型
    address = Field(output_processor=TakeFirst())  # 地址

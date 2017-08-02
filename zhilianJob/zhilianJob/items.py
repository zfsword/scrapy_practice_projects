# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join


class ZhilianjobItem(Item):
    jobName = Field(output_processor=TakeFirst())  # 职位名称1
    welfare = Field()  # 福利待遇1
    salary = Field(output_processor=TakeFirst())  # 工资1
    releaseTime = Field(output_processor=TakeFirst())  # 发布时间
    jobNature = Field(output_processor=TakeFirst())  # 工作性质1
    experience = Field(output_processor=TakeFirst())  # 工作经验1
    education = Field(output_processor=TakeFirst())  # 学历1
    numOfHiring = Field(output_processor=TakeFirst())  # 招聘人数1
    jobCategory = Field(output_processor=TakeFirst())  # 职位类别
    jobDescribe = Field(output_processor=TakeFirst())  # 工作描述1
    workPlace = Field(output_processor=Join())  # 工作地点1

    companyName = Field(output_processor=TakeFirst())  # 公司名称1
    companySize = Field(output_processor=TakeFirst())  # 企业规模1
    companyType = Field(output_processor=TakeFirst())  # 企业类型1
    inderstry = Field(output_processor=TakeFirst())  # 公司行业1
    # finance = Field()  # 资金状况
    companyDescribe = Field(output_processor=Join())  # 公司描述1
    # address = Field()  # 地址

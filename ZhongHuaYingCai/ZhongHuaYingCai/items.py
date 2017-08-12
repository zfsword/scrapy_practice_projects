# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join



class ZhonghuayingcaiItem(Item):
    jobName = Field(output_processor=TakeFirst())
    salary = Field(output_processor=TakeFirst())
    jobLocation = Field(output_processor=TakeFirst())
    jobType = Field(output_processor=TakeFirst())
    education = Field(output_processor=TakeFirst())
    experience = Field(output_processor=TakeFirst())
    jobTags = Field()
    jobDescribe = Field(output_processor=Join())

    companyName = Field(output_processor=TakeFirst())
    inderstry = Field(output_processor=TakeFirst())
    companySize = Field(output_processor=TakeFirst())
    companyTpye = Field(output_processor=TakeFirst())
    companyDescribe = Field(output_processor=Join())

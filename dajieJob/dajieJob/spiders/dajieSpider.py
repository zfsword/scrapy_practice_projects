# -*- coding: utf-8 -*-
import json
import re, time
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchAttributeException

from dajieJob.items import DajiejobItem


class DajiespiderSpider(Spider):
    name = 'dajieSpider'
    allowed_domains = ['dajie.com']
    # start_urls = ['http://dajie.com/']

    # def __init__(self, *args, **kwargs):
    #     super(DajiespiderSpider, self).__init__(*args, **kwargs)

    driver = webdriver.PhantomJS(
        executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver.set_window_size(1400, 900)
    wait = WebDriverWait(driver, 10)

    url = 'http://so.dajie.com/job/search?keyword={kw}&from=job&clicktype=blank&city={city}#{page}'
    kw = 'python'
    city = '110000'
    page = '1'


    def search(self):
        try:
            # self.driver.get('https://www.dajie.com')
            self.driver.get(self.url.format(
                kw=self.kw, city=self.city, page=self.page))

            # return total.text
        # except TimeoutError as e:
        except TimeoutException as e:
            print("Selenium Timeout" + e)
            self.driver.close()
        except (NoSuchAttributeException, NoSuchElementException):
            print("Selenium Find Error")
            self.driver.close()
        # finally:
        #     self.driver.quit()

    def get_job_url(self):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.jobName")))
            return elements
        except TimeoutException:
            print("Selenium Timeout")
            self.driver.close()
        except (NoSuchAttributeException, NoSuchElementException):
            print("Selenium Find Error")
            self.driver.close()

    def start_requests(self):
        self.search()

        # jQueryStopped = self.wait.until(lambda s: s.execute_script("return jQuery.active == 0"))
        # try:
        #     documentReady = self.wait.until(lambda s: s.execute_script("return document.readyState == 'complete'"))
        # except TimeoutException:
        #     print("document not ready")
        # jobList = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.jobList')))
        # container = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#container_jobList')))
        try:
            lastPage = int(self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#page-con"))).get_attribute("lastpage"))
            print("last Page is ", lastPage)
        except (TimeoutException, NoSuchElementException):
            print("Can't find last Page")

        currentPage = 1
        while currentPage < lastPage:

            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")


            urls = self.get_job_url()
            for url in urls:
                print("Job url is " + url.get_attribute("href"))
                yield Request(url.get_attribute("href"), callback=self.parse_detail)

            try:
                nextPage = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="paging"]/a[@class="next"]')))
                nextPage.click()
                time.sleep(3)
            except TimeoutException as e:
                print("Selenium Timeout" + e)
                self.driver.close()
            except (NoSuchAttributeException, NoSuchElementException):
                print("Selenium Find Error")
                self.driver.close()

            currentPage = int(self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#page-con span.current"))).text)
            print("current page is ", currentPage)

        # try:
        #     self.wait.until(EC.staleness_of(jobList))
        # except TimeoutException:
        #     print("staleness job list load time out")



    def parse_detail(self, response):
        item = ItemLoader(item=DajiejobItem(), response=response)
        item.add_css('jid', '.dj-content-shadow input[name=jid]::attr("value")')
        item.add_css('jobName', '.job-msg-top-text .job-name::text')
        item.add_css('salary', '.job-money::text')
        item.add_css('recruit', '.job-msg-center .recruiting span::text', TakeFirst(), lambda s: s.replace(u'\xa0', u' '))
        item.add_css('experience', '.job-msg-center .exp span::text')
        item.add_css('jobTags', '.job-msg-bottom li::text')
        item.add_css('releaseTime', '.job-msg-bottom .date::text')
        item.add_css('jobDescribe', '#jp_maskit pre:nth-child(5)::text', TakeFirst(), lambda s: s.replace(u'\xa0', u' '))
        item.add_css('workPlace', '.ads-msg span::text')
        item.add_css('companyName', '.i-corp-base-info .title a::text')
        item.add_css('companySize', '.i-corp-base-info .info li:nth-child(1) span::text')
        item.add_css('inderstry', '.i-corp-base-info .info li:nth-child(2) span::text')
        item.add_css('companyType', '.i-corp-base-info .info li:nth-child(3) span::text')
        item.add_css('website', '.i-corp-base-info .info li:nth-child(4) a::text')
        item.add_css('companyDescribe', '.i-corp-desc p::text')
        return item.load_item()

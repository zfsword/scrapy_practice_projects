# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException,\
                                    TimeoutException
import unittest, time, re


class DajieWebdriver(unittest.TestCase):
    def setUp(self):
        # self.chromeOptions = webdriver.ChromeOptions()
        # self.chromeOptions.binary_location = r'F:\Program Files\ChromeUpdater\chrome.exe'
        # self.driver = webdriver.Chrome(r'D:\chromedriver_win32\chromedriver.exe', chrome_options=self.chromeOptions)

        self.firefoxBin = webdriver.firefox.firefox_binary.FirefoxBinary(r'F:\Program Files\firefox\firefox.exe')
        # self.firefoxProfile = webdriver.firefox.firefox_profile.FirefoxProfile(r'F:\Program Files\RunningCheese_Firefox_V8\Profiles')
        # self.driver = webdriver.Firefox(firefox_binary=self.firefoxBin, executable_path=r'D:\geckodriver-win64\geckodriver.exe', firefox_profile=self.firefoxProfile)
        self.driver = webdriver.Firefox(firefox_binary=self.firefoxBin, executable_path=r'D:\geckodriver-win64\geckodriver.exe')

        # self.driver= webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        self.driver.implicitly_wait(10)

        self.wait = WebDriverWait(self.driver, 10)

        self.base_url = "https://www.dajie.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

        self.url = 'http://so.dajie.com/job/search?keyword={kw}&from=job&clicktype=blank&city={city}#{page}'
        self.kw = 'python'
        self.city = '110000'
        self.page = '1'
        self.totalPage = 0

    def test_dajie_webdriver(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_id("qzInput").click()
        driver.find_element_by_id("qzInput").clear()
        driver.find_element_by_id("qzInput").send_keys("python")
        driver.find_element_by_id("qzInput").send_keys(Keys.ENTER)
        # driver.find_element_by_id("soqzJob").click()

        beforeWindow = driver.window_handles[0]
        driver.switch_to.window(driver.window_handles[1])
        print(driver.title)

        try:
            lastPage = int(self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#page-con"))).get_attribute("lastpage"))
            print("last Page is ", lastPage)
        except (TimeoutException, NoSuchElementException):
            print("Can't find last Page")

        driver.set_page_load_timeout(10)
        driver.set_script_timeout(5)


        # print(self.driver.execute_script("return jQuery.active == 0"))
        # print(self.driver.execute_script("return document.readyState"))
        jQueryStopped = self.wait.until(lambda s: s.execute_script("return jQuery.active == 0"))
        try:
            documentReady = self.wait.until(lambda s: s.execute_script("return document.readyState == 'complete'"))
        except TimeoutException:
            print("document not ready")

        jobList = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.jobList')))
        container = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#container_jobList')))

        # try:
        #     self.wait.until(EC.staleness_of(jobList))
        # except TimeoutException:
        #     print("staleness job list load time out")


        currentPage = 1

        while currentPage < lastPage:

            jobs = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.jobName")))

            for job in jobs:
                print(job.get_attribute('href'))

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # driver.find_element_by_class_name('next').click()
            try:
                nextPage = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next')))
                nextPage.click()
                time.sleep(3)
            except NoSuchElementException:
                print("Find next page error")
                break
            except TimeoutException:
                print("Find next page time out")
                break

            currentPage = int(self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#page-con span.current"))).text)
            print("current page is ", currentPage)



    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True


    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()

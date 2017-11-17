# -*- coding: utf-8 -*-
import scrapy
from parsel import Selector
from scrapy.utils.response import open_in_browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
from ..items import Paper


# scrapy crawl ieee -a term=5G
class IeeeSpider(scrapy.Spider):
    name = 'ieee'
    allowed_domains = ['ieee.org']
    start_urls = ['http://ieeexplore.ieee.org/']

    def __init__(self, term=None, *args, **kwargs):
        super(IeeeSpider, self).__init__(*args, **kwargs)
        self.term = term

        self.output = []

    def __del__(self):
        self.driver.close()


    def parse(self, response):
        driver = self.driver

        # driver = webdriver.Chrome()

        # 把关键词敲进去开始搜索
        driver.maximize_window()
        driver.find_element_by_xpath("""//*[(@id = "input-basic")]""").send_keys(self.term)
        driver.find_element_by_xpath\
            ("""//*[contains(concat( " ", @class, " " ), concat( " ", "Search-submit-icon", " " ))]""").click()
        time.sleep(4)

        # 搞来搜索的结果
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
        titles = Selector(text=driver.page_source).xpath\
            ("""//h2//*[contains(concat( " ", @class, " " ), concat( " ", "ng-scope", " " ))]""").extract()
        for title_element in titles:
            bs_obj = BeautifulSoup(title_element, 'lxml')
            title_tags = bs_obj.find_all(text=True)
            for title in title_tags:
                paper = Paper()
                paper['title'] = str(title)
                yield paper

        # 下一页走起
        driver.find_element_by_xpath \
            ("""//*[contains(concat( " ", @class, " " ), concat( " ", "next", " " ))][not(contains(@class, "disabled"))]//*[contains(concat( " ", @class, " " ), concat( " ", "ng-binding", " " ))]""").click()
        time.sleep(4)

        try:
            while(True):

                # 搞来搜索结果
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4);")
                titles = Selector(text=driver.page_source).xpath \
                    ("""//h2//*[contains(concat( " ", @class, " " ), concat( " ", "ng-scope", " " ))]""").extract()
                for title_element in titles:
                    bs_obj = BeautifulSoup(title_element, 'lxml')
                    title_tags = bs_obj.find_all(text=True)
                    for title in title_tags:
                        paper = Paper()
                        paper['title'] = str(title)
                        yield paper

                # 下一页走起
                driver.find_element_by_xpath \
                        ("""//*[contains(concat( " ", @class, " " ), concat( " ", "next", " " ))][not(contains(@class, "disabled"))]//*[contains(concat( " ", @class, " " ), concat( " ", "ng-binding", " " ))]""").click()
                time.sleep(4)

        except:
            print("Successfully Scrapped")





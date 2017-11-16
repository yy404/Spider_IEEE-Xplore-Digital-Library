# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector


class IeeeSpider(scrapy.Spider):
    name = 'ieee'
    allowed_domains = ['ieee.org']
    start_urls = ['http://ieee.org/']

    def parse(self, response):
        

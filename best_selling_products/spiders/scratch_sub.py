# -*- coding: utf-8 -*-
import scrapy
import re

from ..items import Product

class ScratchSubSpider(scrapy.Spider):
    name = 'scratch_sub'
    allowed_domains = ['tw.buy.yahoo.com']
    start_urls = ['https://tw.buy.yahoo.com/']
    site_prefix = 'https://tw.buy.yahoo.com'
    sub_url_list = []

    def start_requests(self):
        urls = [
            # 'https://tw.buy.yahoo.com/?sub=430',
            'https://tw.buy.yahoo.com',
        ]
        for url in urls:
            # request = scrapy.Request(url=url, callback=self.parse_sub)
            request = scrapy.Request(url=url, callback=self.parse_all_sub)
            yield request

    def parse_all_sub(self, response):
        sub_url_list = response.xpath('//a/@href[contains(.,"?sub=")]').extract()
        for sub_url in sub_url_list:
            if re.search(r'^http.*\d$', sub_url) is not None:
                self.sub_url_list.append(sub_url)
        for sub_url in self.sub_url_list:
            self.log(sub_url)
            request = scrapy.Request(url=sub_url, callback=self.parse_sub)
            yield request

    def parse_sub(self, response):
        product_list = []
        hotrank = response.xpath('//div[@id="cl-hotrank"]')
        hotrank_ul_list = hotrank.xpath('.//ul[contains(@class, "pdset")]')
        for index, element in enumerate(hotrank_ul_list):
            product_url = element.xpath('.//li[@class="intro"]/div[@class="text"]/a/@href').extract_first()
            title = element.xpath('.//li[@class="intro"]/div[@class="text"]/a/text()').extract_first()
            price = element.xpath('.//li[@class="intro"]/div[@class="pd-price"]//a/text()').extract_first()
            is_static_page = True
            # filte out none product page
            if title is not None:
                # convert to absolute URL
                if re.search(r'^http', product_url) is None:
                    product_url = self.site_prefix + product_url
                # determine URL is product content page or category list page
                if re.search(r'catitemid=', product_url) is not None:
                    is_static_page = False
                if re.search(r'sub=', product_url) is not None:
                    is_static_page = False
                product = Product(title=title, url=product_url, price=price, is_static_page=is_static_page)
                if is_static_page:
                    product_list.append(product)

        for product in product_list:
            request = scrapy.Request(url=product['url'], callback=self.parse_product_page)
            request.meta['item'] = product
            yield request

    def parse_product_page(self, response):
        product = response.meta['item']
        category = response.xpath('//h3[@itemprop="title"]/text()').extract_first()
        product['category'] = category
        return product

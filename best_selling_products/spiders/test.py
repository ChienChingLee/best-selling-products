# -*- coding: utf-8 -*-
import scrapy
import re

from ..items import Product

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['tw.buy.yahoo.com']
    start_urls = ['https://tw.buy.yahoo.com/']
    site_prefix = 'https://tw.buy.yahoo.com'

    def start_requests(self):
        urls = [
            # 'https://tw.buy.yahoo.com/?sub=430',
            'https://tw.buy.yahoo.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        product_list = []
        hotsale = response.xpath('//div[@id="hotsale"]')
        self.log(hotsale.extract_first())
        hotsale_a_list = hotsale.xpath('.//a')
        for element in hotsale_a_list:
            product_url = element.xpath('@href').extract_first()
            title = element.xpath('div[@class="desc"]/text()').extract_first()
            price = element.xpath('.//span[@class="shpprice"]/text()').extract_first()
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
                product = Product(title, product_url, price, is_static_page)
                product_list.append(product)

        # for debug
        for product in product_list:
            self.log(product)
            # self.log('title: %s' % product.title)
            # self.log('url: %s' % product.url)
            # self.log('price: %s' % product.price)
            # self.log('is_static_page: %s' % product.is_static_page)
        self.log('===============parse end===============')
    # def parse(self, response):
    #     page = response.url.split("?")[-1]
    #     category_num = page.split("=")[1]
    #     filename = 'category-%s.html' % category_num
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

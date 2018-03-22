# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter

class BestSellingProductsPipeline(object):

    def process_item(self, item, spider):
        print(item.items())
        return item

class BestSellingProductsPipelineExportCSV(object):

    def open_spider(self, spider):
        f = open('/best-selling-products/output/output.csv', 'w+b')
        self.exporter = CsvItemExporter(f, fields_to_export=['title', 'price', 'category', 'url'])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        print(item.items())
        return item

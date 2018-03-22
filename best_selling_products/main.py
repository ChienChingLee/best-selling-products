# -*- coding: utf-8 -*-
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
settings['LOG_ENABLED'] = False
settings['ITEM_PIPELINES'] = {'best_selling_products.pipelines.BestSellingProductsPipeline': 300}
if sys.argv[1:] and sys.argv[1] == '--export':
    print('export CSV')
    settings['ITEM_PIPELINES'] = {'best_selling_products.pipelines.BestSellingProductsPipelineExportCSV': 300}
process = CrawlerProcess(settings)

process.crawl('scratch_sub')
process.start() # the script will block here until the crawling is finished

FROM python:3.6.4-jessie
MAINTAINER David Lee

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir scrapy
ADD best_selling_products /best_selling_products
ADD scrapy.cfg /scrapy.cfg

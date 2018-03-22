# Best selling products crawler

## Description

Imagine that you want to do algorithm-based e-commerce on domestic market, and targeting on Yahoo store (https://tw.buy.yahoo.com/). The first step is to understand what kind of product sells well on the platform. Like any other storefront, the yahoo's platform has categories and some best selling products. Please write an efficient crawling architecture and a query interface that gets the best selling products from yahoo store:

1. an efficient crawler to get product pricing and category information
1. define and discover how to get the best selling products, explain possible limitations
1. a query interface to operate on crawled data, could be command line tools
1. able to export result in CSV and excel

The code must be written in python, you can put it on github so that we can review your code. Documentation should also be provided to let us know your design, assumption, and what python modules you've used.

You don't need to write too many codes. Try to make it simple, elegant and comprehensive. But your code must be executable and functional workable, pseudo code is not acceptable.

## Discussion
### Approach
By observing web page layout and content, we can define some keyword for search best selling products.

Like:
- main page:
  - 熱銷商品 `<div id="hotsale">`
- category page:
  - 熱門精選 `<div id="cl-hotrank">`

[scrapy 1.5](https://scrapy.org/) used.

### Otherwise
From single crawler/customer perspective, there was no clear way to know e-commerce platform products sales status. Although, we can though few facts to guess how they are. include:
- Have the product hyperlink appeared on the front page?
  (maybe the product is promoting, not mean it selling well.)
- The frequency of Pop-up in the recommended area?
  (maybe the product is promoting, not mean it selling well.)
- Is the product sellout?
  (maybe inventory was very few from beginning)

Retargeting ads effect?

## Feature

- Search all category pages hot rank products from the main page started.

## Install
### Requirement

- Docker 17.12.0+ on x86 arch

### Docker Image

- build
  - `docker build -t s80275/best-selling-products:v1.0.0 .`
- or just pull from docker hub
  - `docker pull s80275/best-selling-products:v1.0.0`

### Run
- display on console:
`docker run --rm s80275/best-selling-products:v1.0.0 python /best_selling_products/main.py`
- export CSV file
`docker run --rm -v <your_output_dir>:/best-selling-products/output s80275/best-selling-products:v1.0.0 python /best_selling_products/main.py --export`

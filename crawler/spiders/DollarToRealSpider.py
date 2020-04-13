# -*- coding: utf-8 -*-
import scrapy

from crawler.items import QuotationItem

# Spider responsável pela cotação do Dolar em relação ao Real
class DollarToRealSpider(scrapy.Spider):
    name = 'DollarToRealSpider'
    allowed_domains = ['m.investing.com']
    start_urls = ['https://m.investing.com/currencies/usd-brl']

    def parse(self, response):
        sel = scrapy.Selector(response)
        result = sel.css(".quotesBox")

        VALUE_SELECTOR = "./div[contains(@class, 'quotesBoxTop')]/span[contains(@class, 'lastInst ')]/text()"
        CHANGE_SELECTOR = "./div[contains(@class, 'quotesBoxTop')]/span[contains(@class, 'quotesChange')]/i[contains(@class, '-pc')]/text()"
        PERC_SELECTOR = "./div[contains(@class, 'quotesBoxTop')]/span[contains(@class, 'quotesChange')]/i[contains(@class, '-pcp')]/text()"
        TIMESTAMP_SELECTOR = "./div[contains(@class, 'pairTimestamp')]/i[contains(@class, '-time')]/text()"

        value = result.xpath(VALUE_SELECTOR).extract_first().strip()
        change = result.xpath(CHANGE_SELECTOR).extract_first().strip()
        perc = result.xpath(PERC_SELECTOR).extract_first().strip()
        timestamp = result.xpath(TIMESTAMP_SELECTOR).extract_first().strip()

        item = QuotationItem(currency = 'BRL', value = value, change = change, perc = perc, timestamp = timestamp)
        
        yield item
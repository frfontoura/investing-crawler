# -*- coding: utf-8 -*-
import scrapy

from crawler.items import NasdaqItem

# Spider responsável pela busca das ações listadas na Nasdaq
class NasdaqSpider(scrapy.Spider):
    name = 'NasdaqSpider'
    allowed_domains = ['investing.com']
    start_urls = ['https://www.investing.com/equities/StocksFilter?index_id=20']

    def parse(self, response):
        sel = scrapy.Selector(response)
        results = sel.xpath("//*[contains(@id, 'pair_')]")
        for result in results:
            NAME_SELECTOR = "./td/a/text()"
            LAST_SELECTOR = "./td[contains(@class, '-last')]/text()"
            HIGH_SELECTOR = "./td[contains(@class, '-high')]/text()"
            LOW_SELECTOR = "./td[contains(@class, '-low')]/text()"
            CHG_SELECTOR = "./td[contains(@class, '-pc')]/text()"
            CHG_PER_SELECTOR = "./td[contains(@class, '-pcp')]/text()"
            VOL_SELECTOR = "./td[contains(@class, '-turnover')]/text()"
            TIME_SELECTOR = "./td[contains(@class, '-time')]/text()"

            name = result.xpath(NAME_SELECTOR).extract_first()
            last = result.xpath(LAST_SELECTOR).extract_first()
            high = result.xpath(HIGH_SELECTOR).extract_first()
            low = result.xpath(LOW_SELECTOR).extract_first()
            chg = result.xpath(CHG_SELECTOR).extract_first()
            chg_per = result.xpath(CHG_PER_SELECTOR).extract_first()
            vol = result.xpath(VOL_SELECTOR).extract_first()
            time = result.xpath(TIME_SELECTOR).extract_first()
            
            item = NasdaqItem(name=name, last_usd=last, high_usd=high, low_usd=low, chg=chg, chg_per=chg_per, vol=vol, time=time)

            yield item
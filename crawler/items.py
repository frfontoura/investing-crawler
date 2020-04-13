# -*- coding: utf-8 -*-
import scrapy

# Representa um item default com os dados de um determinado ativo
class DefaultStockItem(scrapy.Item):
    name = scrapy.Field()
    last_rs = scrapy.Field()
    high_rs = scrapy.Field()
    low_rs = scrapy.Field()
    chg = scrapy.Field()
    chg_per = scrapy.Field()
    vol = scrapy.Field()
    time = scrapy.Field()

# Representa um item referente a um ativo do Ibovespa
class IbovespaItem(DefaultStockItem):
    pass

# Representa um item referente a um ativo da Nasdaq
class NasdaqItem(DefaultStockItem):
    last_usd = scrapy.Field()
    high_usd = scrapy.Field()
    low_usd = scrapy.Field()

# Representa um item de cotação do Dolar em relação ao Real
class QuotationItem(scrapy.Item):
    currency = scrapy.Field()
    value = scrapy.Field()
    change = scrapy.Field()
    perc = scrapy.Field()
    timestamp = scrapy.Field()
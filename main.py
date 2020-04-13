import schedule
import time
import sqlite3
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from crawler.spiders.IbovespaSpider import IbovespaSpider
from crawler.spiders.DollarToRealSpider import DollarToRealSpider
from crawler.spiders.NasdaqSpider import NasdaqSpider

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)

# Inicializa o processo
@defer.inlineCallbacks
def crawl():
  yield runner.crawl(IbovespaSpider)
  yield runner.crawl(DollarToRealSpider)
  yield runner.crawl(NasdaqSpider)
  showLastUpdates()
  reactor.callLater(120, crawl)

# Exibe os ultimos resultados das tabelas ibovespa_stocks, nasdaq_stocks e dollar_quotation
def showLastUpdates():
  conn = sqlite3.connect('crawler.db')
  c = conn.cursor()

  print('########## IBOVESPA STOCKS ##########')
  for row in c.execute('SELECT * FROM (SELECT * FROM ibovespa_stocks ORDER BY id DESC limit 73) ORDER BY id'):
    print(row)

  print('########## DOLLAR QUOTATION #########')
  for row in c.execute('SELECT * FROM dollar_quotation ORDER BY id DESC limit 1'):
    print(row)

  print('########## NASDAQ STOCKS ############')
  for row in c.execute('SELECT * FROM (SELECT * FROM nasdaq_stocks ORDER BY id DESC limit 103) ORDER BY id'):
    print(row)

  conn.close()


crawl()
reactor.run()
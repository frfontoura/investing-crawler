# -*- coding: utf-8 -*-
import sqlite3
from crawler.items import IbovespaItem, NasdaqItem, QuotationItem
from decimal import Decimal

# Pipeline responsavel pelo tratamento dos dados obtidos pelo IbovespaSpider
class IbovespaPipeline(object):

    # Cria uma conexão com o banco de dados e cria a tabela ibovespa_stocks caso não exista
    def open_spider(self, spider):
        self.conn = sqlite3.connect('crawler.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ibovespa_stocks(id INTEGER PRIMARY KEY, name text, last_rs text, high_rs text, low_rs text, chg text, chg_per text, vol text, time text)''')

    # Realiza o commit das transações e fecha a conexão com o banco
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    # Verifica se é um item do tipo IbovespaItem, caso seja salva no banco de dados
    def process_item(self, item, spider):
        if not isinstance(item, IbovespaItem):
            return item
        
        self.cursor.execute("insert into ibovespa_stocks (name, last_rs, high_rs, low_rs, chg, chg_per, vol, time) values (?, ?, ?, ?, ?, ?, ?, ?)", 
            (item['name'], 
            item['last_rs'], 
            item['high_rs'], 
            item['low_rs'], 
            item['chg'], 
            item['chg_per'], 
            item['vol'], 
            item['time']))

        return item

# Pipeline responsavel pelo tratamento dos dados obtidos pelo DollarToRealSpider
class DollarToRealPipeline(object):
    
    # Cria uma conexão com o banco de dados e cria a tabela dollar_quotation caso não exista
    def open_spider(self, spider):
        self.conn = sqlite3.connect('crawler.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dollar_quotation(id INTEGER PRIMARY KEY, currency text, value text, change text, perc text, timestamp text)''')

    # Realiza o commit das transações e fecha a conexão com o banco
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    # Verifica se é um item do tipo QuotationItem, caso seja salva no banco de dados
    def process_item(self, item, spider):
        if not isinstance(item, QuotationItem):
            return item

        self.cursor.execute("insert into dollar_quotation(currency, value, change, perc, timestamp) values (?, ?, ?, ?, ?)", 
            (item['currency'], 
            item['value'], 
            item['change'], 
            item['perc'], 
            item['timestamp']))

        return item

# Pipeline responsavel pelo tratamento dos dados obtidos pelo NasdaqSpider
class NasdaqPipeline(object):
    
    # Cria uma conexão com o banco de dados e cria a tabela nasdaq_stocks caso não exista
    def open_spider(self, spider):
        self.conn = sqlite3.connect('crawler.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS nasdaq_stocks(id INTEGER PRIMARY KEY, name text, last_rs text, high_rs text, low_rs text, chg text, chg_per text, vol text, time text, last_usd text, high_usd text, low_usd text)''')

    # Realiza o commit das transações e fecha a conexão com o banco
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    # Verifica se é um item do tipo NasdaqItem, caso seja, calcula o valor em reais baseado na ultima cotação do dolar e salva no banco de dados
    def process_item(self, item, spider):
        if not isinstance(item, NasdaqItem):
            return item

        row = self.cursor.execute('SELECT value FROM dollar_quotation ORDER BY id desc limit 1').fetchone()
        value = Decimal(row[0]) if row else 0
        last_rs = round(Decimal(item['last_usd'].replace(',', '')) * value ,2)
        high_rs = round(Decimal(item['high_usd'].replace(',', '')) * value ,2)
        low_rs = round(Decimal(item['low_usd'].replace(',', '')) * value ,2)

        item['last_rs'] = str(last_rs)
        item['high_rs'] = str(high_rs)
        item['low_rs'] = str(low_rs)
        
        self.cursor.execute("insert into nasdaq_stocks (name, last_rs, high_rs, low_rs, chg, chg_per, vol, time, last_usd, high_usd, low_usd) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (item['name'], 
            item['last_rs'], 
            item['high_rs'], 
            item['low_rs'], 
            item['chg'], 
            item['chg_per'], 
            item['vol'], 
            item['time'], 
            item['last_usd'], 
            item['high_usd'], 
            item['low_usd']))

        return item

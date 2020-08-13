import requests
from bs4 import BeautifulSoup
import json

def getUrl(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    api = requests.get(url, headers = header)
    api_json = json.loads(api.text)
    return api_json

def huobi():
    try:
        ex = []
        url = 'https://api.hadax.com/v1/common/symbols'
        api_json = getUrl(url)
        for s in api_json['data']:
            ex.append([(s['base-currency']+"/"+s['quote-currency']).upper() , s['base-currency'].upper() , s['quote-currency'].upper()])
        return ex
    except:
        return []

def bitfinex():
    try:
        ex = []
        url = 'https://api.bitfinex.com/v1/symbols'
        api_json = getUrl(url)
        for s in api_json:
            ex.append([s[:3]+"/"+s[-3:], s[:3], s[-3:]])
        return ex
    except:
        return []

def bittrex():
    try:
        ex = []
        url = 'https://bittrex.com/api/v1.1/public/getmarkets'
        api_json = getUrl(url)
        for s in api_json['result']:
            ex.append([s['MarketCurrency']+"/"+s['BaseCurrency'], s['MarketCurrency'], s['BaseCurrency']])
        return ex
    except:
        return []

def bit_z():
    try:
        ex = []
        url = 'https://www.bit-z.com/api_v1/tickerall'
        api_json = getUrl(url)
        for s in api_json['data']:
            a,b = s.upper().split('_')
            ex.append([a+"/"+b, a, b])
        return ex
    except:
        return []

def binance():
    try:
        ex = []
        url = 'https://api.binance.com/api/v1/exchangeInfo'
        api_json = getUrl(url)
        for s in api_json['symbols']:
            ex.append([s['baseAsset']+"/"+s['quoteAsset'] , s['baseAsset'] , s['quoteAsset']])
        return ex
    except:
        return []

def gdax():
    try:
        ex = []
        url = 'https://api.gdax.com/products'
        api_json = getUrl(url)
        for s in api_json:
            ex.append([s['base_currency']+"/"+s['quote_currency'] , s['base_currency'] , s['quote_currency']])
        return ex
    except:
        return []

def hadax():
    try:
        ex = []
        url = 'https://api.hadax.com/v1/hadax/common/symbols'
        api_json = getUrl(url)
        for s in api_json['data']:
            ex.append([s['base-currency'].upper()+"/"+s['quote-currency'].upper() , s['base-currency'].upper() , s['quote-currency'].upper()])
        return ex
    except:
        return []

def hitbtc():
    try:
        ex = []
        url = 'https://api.hitbtc.com/api/2/public/symbol'
        api_json = getUrl(url)
        for s in api_json:
            ex.append([s['baseCurrency']+"/"+s['quoteCurrency'], s['baseCurrency'], s['quoteCurrency']])
        return ex
    except:
        return []

def kucoin():
    try:
        ex = []
        url = 'https://api.kucoin.com/v1/market/open/symbols'
        api_json = getUrl(url)
        for s in api_json['data']:
            ex.append([s['coinType']+"/"+s['coinTypePair'] , s['coinType'] , s['coinTypePair']])
        return ex
    except:
        return []

def bithumb():
    try:
        ex = []
        url = 'https://www.bithumb.com/resources/csv/market_sise.json'
        api_json = getUrl(url)
        for s in api_json:
            ex.append([s['symbol'], s['symbol'], '-'])
        return ex
    except:
        return []

def upbit():
    try:
        ex = []
        url = 'https://s3.ap-northeast-2.amazonaws.com/crix-production/crix_master'
        api_json = getUrl(url)
        for s in api_json:
            ex.append([s['pair'], s['baseCurrencyCode'], s['quoteCurrencyCode']])
        return ex
    except:
        return []

def gopax():
    try:
        ex = []
        url = 'https://api.gopax.co.kr/trading-pairs'
        api_json = getUrl(url)
        for s in api_json:
            ex.append([s['baseAsset']+"/"+s['quoteAsset'], s['baseAsset'], s['quoteAsset']])
        return ex
    except:
        return []
        

# print(gopax())
# print(upbit())

#print(bithumb())


#print(kucoin())
# print(hitbtc())
# print(huobi())
# print(hadax())
# print(gdax())
#print(binance())

# print(bit_z())
#bittrex()
# bitfinex()
#huobi()

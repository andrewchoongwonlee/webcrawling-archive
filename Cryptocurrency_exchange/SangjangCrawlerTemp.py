import requests
from bs4 import BeautifulSoup
import json

def huobi(api_json):
    try:
        for s in api_json['data']:
            ex.append([(s['base-currency']+"/"+s['quote-currency']).upper() , s['base-currency'].upper() , s['quote-currency'].upper()])
        return ex
    except:
        return []

def bitfinex(api_json):
    try:
        for s in api_json:
            ex.append([s[:3]+"/"+s[-3:], s[:3], s[-3:]])
        return ex
    except:
        return []

def bittrex(api_json):
    try:
        for s in api_json['result']:
            ex.append([s['MarketCurrency']+"/"+s['BaseCurrency'], s['MarketCurrency'], s['BaseCurrency']])
        return ex
    except:
        return []

def bit_z(api_json):
    try:
        for s in api_json['data']:
            a,b = s.upper().split('_')
            ex.append([a+"/"+b, a, b])
        return ex
    except:
        return []

def binance(api_json):
    try:
        for s in api_json['symbols']:
            ex.append([s['baseAsset']+"/"+s['quoteAsset'] , s['baseAsset'] , s['quoteAsset']])
        return ex
    except:
        return []

def gdax(api_json):
    try:
        for s in api_json:
            ex.append([s['base_currency']+"/"+s['quote_currency'] , s['base_currency'] , s['quote_currency']])
        return ex
    except:
        return []

def hadax(api_json):
    try:
        for s in api_json['data']:
            ex.append([s['base-currency'].upper()+"/"+s['quote-currency'].upper() , s['base-currency'].upper() , s['quote-currency'].upper()])
        return ex
    except:
        return []

def hitbtc(api_json):
    try:
        for s in api_json:
            ex.append([s['baseCurrency']+"/"+s['quoteCurrency'], s['baseCurrency'], s['quoteCurrency']])
        return ex
    except:
        return []

def kucoin(api_json):
    try:
        for s in api_json['data']:
            ex.append([s['coinType']+"/"+s['coinTypePair'] , s['coinType'] , s['coinTypePair']])
        return ex
    except:
        return []

def bithumb(api_json):
    try:
        for s in api_json:
            ex.append([s['symbol'], s['symbol'], '-'])
        return ex
    except:
        return []

def upbit(api_json):
    try:
        for s in api_json:
            ex.append([s['pair'], s['baseCurrencyCode'], s['quoteCurrencyCode']])
        return ex
    except:
        return []

def gopax(api_json):
    try:
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

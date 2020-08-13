import requests
from bs4 import BeautifulSoup as bs
import pymysql
import time
import json
from functools import partial

from multiprocessing import Pool , Manager
# personal
# import SangjangCrawlerTemp as fetchdata
import SangjangBotApi

def sendMessage(exchange, new):
    tg.sendPlain('[%s] 신규 거래쌍(코인) 상장 감지\n%s'%(exchange, new))

def compareDB(e, ex):
    try:
        new = []
        sql = "SELECT * from "+ex
        if len(ex) == curs.execute(sql):
            pass
        else:
            for i in range(len(datas[ex])):
                sql = "SELECT pair from "+ex+" where pair = %s"
                if curs.execute(sql, (ex[i][0])) > 0:
                    pass
                else:
                    new.append(ex[i][0])
                    sql = "INSERT INTO "+ex+" (pair, base, quote) VALUES (%s, %s, %s)"
                    curs.execute(sql, (ex[i][0], ex[i][1], ex[i][2]))
                    conn.commit()
        except:
            pass
        try:
            if len(new) > 0:
                print('['+ex+'] %d new pairs ... '%(len(new)))
                for n in new:
                    sendMessage(e, i)
            else:
                pass
        except:
            pass

def get_json(link):
    while(True):
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
            api = requests.get(link[1], headers = header)
            api_json = json.loads(api.text)
            jsons[link[0]] = api_json
        except:
            print('Api error retrying')
        else:
            break

def parse_data(e):
    ex = []
    if e == 'bitfinex':
        try:
            for s in jsons[e]:
                ex.append([s[:3].upper()+"/"+s[-3:].upper(), s[:3].upper(), s[-3:].upper()])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'bittrex':
        try:
            for s in jsons[e]['result']:
                ex.append([s['MarketCurrency']+"/"+s['BaseCurrency'], s['MarketCurrency'], s['BaseCurrency']])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'bit_z':
        try:
            for s in jsons[e]['data']:
                a,b = s.upper().split('_')
                ex.append([a+"/"+b, a, b])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'binance':
        try:
            for s in jsons[e]['symbols']:
                ex.append([s['baseAsset']+"/"+s['quoteAsset'] , s['baseAsset'] , s['quoteAsset']])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'gdax':
        try:
            for s in jsons[e]:
                ex.append([s['base_currency']+"/"+s['quote_currency'] , s['base_currency'] , s['quote_currency']])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'hadax':
        try:
            for s in jsons[e]['data']:
                ex.append([s['base-currency'].upper()+"/"+s['quote-currency'].upper() , s['base-currency'].upper() , s['quote-currency'].upper()])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'huobi':
        try:
            for s in jsons[e]['data']:
                ex.append([(s['base-currency']+"/"+s['quote-currency']).upper() , s['base-currency'].upper() , s['quote-currency'].upper()])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'hitbtc':
        try:
            for s in jsons[e]['symbols']:
                ex.append([s['commodity']+"/"+s['currency'], s['commodity'], s['currency']])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'kucoin':
        try:
            for s in jsons[e]['data']:
                ex.append([s['coinType']+"/"+s['coinTypePair'] , s['coinType'] , s['coinTypePair']])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'bithumb':
        try:
            for s in jsons[e]:
                ex.append([s['symbol'], s['symbol'], '-'])
        except:
            pass:
        compareDB(e, ex)

    elif e == 'upbit':
        try:
            for s in jsons[e]:
                if s['exchange'] == 'UPBIT':
                    ex.append([s['pair'], s['baseCurrencyCode'], s['quoteCurrencyCode']])
                else:
                    pass
        except:
            pass:
        compareDB(e, ex)

    elif e == 'gopax':
        try:
            for s in jsons[e]:
                ex.append([s['baseAsset']+"/"+s['quoteAsset'], s['baseAsset'], s['quoteAsset']])
        except:
            pass:
        compareDB(e, ex)

if __name__=='__main__':
    conn = pymysql.connect(host='localhost', user='root', password='yewon0527', charset='utf8')
    curs = conn.cursor()
    sql = "USE pair"
    curs.execute(sql)
    tg = SangjangBotApi.TelegramBot()

    urls = [
    #['bitfinex' , 'https://api.bitfinex.com/v1/symbols'],
    ['bittrex' , 'https://bittrex.com/api/v1.1/public/getmarkets'],
    ['bit_z' , 'https://www.bit-z.com/api_v1/tickerall'],
    ['binance' , 'https://api.binance.com/api/v1/exchangeInfo'],
    ['gdax' , 'https://api.gdax.com/products'],
    ['hadax' , 'https://api.hadax.com/v1/hadax/common/symbols'],
    ['huobi' , 'https://api.hadax.com/v1/common/symbols'],
    ['hitbtc' , 'https://api.hitbtc.com/api/1/public/symbols'],
    ['kucoin' , 'https://api.kucoin.com/v1/market/open/symbols'],
    ['bithumb' , 'https://www.bithumb.com/resources/csv/market_sise.json'],
    ['upbit' , 'https://s3.ap-northeast-2.amazonaws.com/crix-production/crix_master'],
    ['gopax' , 'https://api.gopax.co.kr/trading-pairs']
    ]

    exch = []
    for s in urls:
        exch.append(s[0])

    mng1 = Manager()
    mng2 = Manager()

    while(True):
        start_time = time.time()
        jsons = mng1.dict()
        pool = Pool(processes=8)
        pool.map(get_json, urls)
        pool.close()



        ## Parse
        datas = mng2.dict()
        pool2 = Pool(processes=8)
        pool2.map(parse_data, exch)
        pool2.close()


        print("--- %.3s seconds ---" % (time.time() - start_time))


    conn.close()

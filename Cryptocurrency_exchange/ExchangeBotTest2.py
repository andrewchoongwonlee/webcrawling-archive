from multiprocessing import Pool
from multiprocessing import Manager
from bs4 import BeautifulSoup as bs
import requests
import pymysql
import time
import json


import ExchangeBotApi
import pymysql

def sendMessage(exchange, title, url):
    tg.sendPlain('[%s] 거래소 공지\n<a href="%s">%s</a>'%(exchange, url, title))

def compareDB(e, ex):
    new = []
    for s in ex:
        sql = "SELECT title from "+ e +" where title = %s"
        if curs.execute(sql, (s[0]) > 0:
            pass
        else:
            new.append([s[0], s[1]])
            sql = "INSERT INTO "+e+" (title, url) VALUES (%s, %s)"
            curs.execute(sql, (s[0], s[1]))
            conn.commit()

    try:
        if len(new) > 0:
            print('['+e+'] %d new pairs ... '%(len(new)))
            for n in new:
                sendMessage(e, n[0], n[1])
        else:
            pass
    except:
        pass

def get_json(link):
    e = link[0]
    url = link[1]
    while(True):
        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
            api = requests.get(url, headers = header)
            api_json = api.json()
        except:
            print('[%s] Api request error.. retrying'%(link[0]))
        else:
            break

    ex = []
    if e == 'bittrex':
        try:
            for s in api_json['articles']:
                ex.append([s['title'], s['html_url']])
        except:
            pass
        compareDB(e, ex)

    elif e == 'binance':
        try:
            for s in api_json['activities']:
                if s['action'] == 'article_created':
                    ex.append([s['title'], 'https://support.binance.com'+str(s['url'])])
        except:
            pass
        compareDB(e, ex)

    elif e == 'bithumb':
        try:
            for s in api_json:
                if s['categories'] == [43]: # 공지
                    ex.append([s['title']['rendered'], s['link']])
        except:
            pass
        compareDB(e, ex)

    elif e == 'upbit':
        try:
            for s in api_json['data']['list']:
                ex.append([s['title'], 'https://www.upbit.com/service_center/notice?id='+str(s['id'])])
        except:
            pass
        compareDB(e, ex)

    elif e == 'bitmex':
        try:
            for s in api_json:
                if s['language'] == [511]: # korean
                    ex.append([s['title']['rendered'], s['link']])
        except:
            pass
        compareDB(e, ex)


if __name__=='__main__':
    conn = pymysql.connect(host='localhost', user='root', password='yewon0527', charset='utf8')
    curs = conn.cursor()
    sql = "USE exchange"
    curs.execute(sql)
    tg = ExchangeBotApi.TelegramBot()

    urls = [
    #['bitfinex' , ''],
    ['bittrex' , 'https://support.bittrex.com/api/v2/help_center/en-us/articles'],
    #['bit_z' , ''],
    ['binance' , 'https://support.binance.com/hc/api/internal/recent_activities?locale=en-us&page=1&per_page=5&locale=en-us'],
    #['gdax' , ''],
    #['hadax' , ''],
    #['huobi' , ''],
    #['hitbtc' , ''],
    #['kucoin' , ''],
    ['bithumb' , 'http://bithumb.cafe/wp-json/wp/v2/posts'],
    ['upbit' , 'https://api-manager.upbit.com/api/v1/notices/'],
    #['gopax' , '']
    ['bitmex', 'https://blog.bitmex.com/wp-json/wp/v2/posts']
    ]

    exch = []
    for s in urls:
        exch.append(s[0])

    while(True):
        try:
            start_time = time.time()
            pool = Pool(processes=1)
            pool.map(get_json, urls)
            pool.close()
            pool.join()

            print("--- %.3s seconds ---" % (time.time() - start_time))
            time.sleep(0.05)

        except KeyboardInterrupt:
            print('pool terminate')
            pool.terminate()
            conn.close()


    conn.close()

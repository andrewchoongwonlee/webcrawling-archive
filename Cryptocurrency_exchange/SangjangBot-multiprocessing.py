import SangjangBotApi
import SangjangCrawler as crawl
import pymysql
import time
import datetime
from multiprocessing import Process

def sendMessage(exchange, new):
    tg.sendPlain('[%s] 신규 거래쌍(코인) 상장 감지\n%s'%(exchange, new))

def compareDB(ex):
    new = []
    sql = "SELECT * from "+ex
    if len(pairs[ex]) == curs.execute(sql):
        pass
    else:
        for i in range(len(pairs[ex])):
            sql = "SELECT pair from "+ex+" where pair = %s"
            if curs.execute(sql, (pairs[ex][i][pair])) > 0:
                pass
            else:
                new.append(pairs[ex][i][pair])
                sql = "INSERT INTO "+ex+" (pair, base, quote) VALUES (%s, %s, %s)"
                curs.execute(sql, (pairs[ex][i][pair], pairs[ex][i][base], pairs[ex][i][quote]))
                conn.commit()
        if len(new) > 0:
            print('['+ex+'] %d new pairs ... '%(len(new)))
    return new

def comp(ex):
    temp = []
    temp = compareDB(ex)
    if len(temp) > 0:
        for i in temp:
            pass
            #cnt+=1
            #sendMessage(ex, i)
    else:
        pass

# def bitfinex():
#     pairs['bitfinex'] = crawl.bitfinex()
#     comp('bitfinex')

def bittrex():
    pairs['bittrex'] = crawl.bittrex()
    comp('bittrex')

def bit_z():
    pairs['bit_z'] = crawl.bit_z()
    comp('bit_z')

def binance():
    pairs['binance'] = crawl.binance()
    comp('binance')

def gdax():
    pairs['gdax'] = crawl.gdax()
    comp('gdax')

def hadax():
    pairs['hadax'] = crawl.hadax()
    comp('hadax')

def huobi():
    pairs['huobi'] = crawl.huobi()
    comp('huobi')

def hitbtc():
    pairs['hitbtc'] = crawl.hitbtc()
    comp('hitbtc')

def kucoin():
    pairs['kucoin'] = crawl.kucoin()
    comp('kucoin')

def bithumb():
    pairs['bithumb'] = crawl.bithumb()
    comp('bithumb')

def upbit():
    pairs['upbit'] = crawl.upbit()
    comp('upbit')

def gopax():
    pairs['gopax'] = crawl.gopax()
    comp('gopax')

if __name__ == "__main__":
    conn = pymysql.connect(host='localhost', user='root', password='yewon0527', charset='utf8')
    curs = conn.cursor()
    sql = "USE pair"
    curs.execute(sql)

    tg = SangjangBotApi.TelegramBot()
    pair = 0
    base = 1
    quote = 2
    while(True):
        now = datetime.datetime.now()
        #exchanges = ['bitfinex','bittrex','bit_z','binance','gdax','hadax','huobi','hitbtc','kucoin','bithumb','upbit','gopax']
        #exchanges = ['kucoin','bithumb','upbit','gopax']
        # exchanges = ['bitfinex','bittrex','bit_z']
        pairs = {}
        # cnt = 0

        # p1 = Process(target=bitfinex)
        p2 = Process(target=bittrex())
        p3 = Process(target=bit_z())
        p4 = Process(target=binance())
        p5 = Process(target=gdax())


        # Process start
        # p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        # p6 = Process(target=hadax())
        # p7 = Process(target=huobi())
        # p8 = Process(target=hitbtc())
        #
        # p6.start()
        # p7.start()
        # p8.start()
        # p6.join()
        # p7.join()
        # p8.join()
        #
        #
        # p9 = Process(target=kucoin())
        # p10 = Process(target=bithumb())
        # p11 = Process(target=upbit())
        # p12 = Process(target=gopax())
        # p9.start()
        # p10.start()
        # p11.start()
        # p12.start()
        #
        #
        # # p1.join()
        #
        # p9.join()
        # p10.join()
        # p11.join()
        # p12.join()

        #p1.terminate()
        # p2.terminate()
        # p3.terminate()
        # p4.terminate()
        # p5.terminate()
        # p6.terminate()
        # p7.terminate()
        # p8.terminate()
        # p9.terminate()
        # p10.terminate()
        # p11.terminate()
        # p12.terminate()

        # pairs = {
        # 'bitfinex' : crawl.bitfinex(),
        # 'bittrex' : crawl.bittrex(),
        # 'bit_z' : crawl.bit_z(),
        # 'binance' : crawl.binance(),
        # 'gdax' : crawl.gdax(),
        # 'hadax' : crawl.hadax(),
        # 'huobi' : crawl.huobi(),
        # 'hitbtc' : crawl.hitbtc(),
        # 'kucoin' : crawl.kucoin(),
        # 'bithumb' : crawl.bithumb(),
        # 'upbit' : crawl.upbit(),
        # 'gopax' : crawl.gopax()
        # }
        #

        # for ex in exchanges:
        #     temp = []
        #     temp = compareDB(ex)
        #     if len(temp) > 0:
        #         for i in temp:
        #             cnt+=1
        #             sendMessage(ex, i)
        #     else:
        #         pass


        print('%s'%(now.strftime('%Y-%m-%d %H:%M:%S')))
        # time.sleep(2)

    conn.close()

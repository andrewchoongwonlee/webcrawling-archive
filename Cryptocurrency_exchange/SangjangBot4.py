import SangjangBotApi
import SangjangCrawler as crawl
import pymysql
import time
import datetime

def sendMessage(exchange, new):
    tg.sendPlain('[%s] 신규 거래쌍(코인) 상장 감지\n%s'%(exchange, new))

def compareDB(ex):
    new = []
    sql = "SELECT * from "+ex
    print(len(pairs[ex]))
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
        exchanges = ['bitfinex']
        #exchanges = ['kucoin','bithumb','upbit','gopax']
        pairs = {}

        pairs = {
        'bitfinex' : crawl.bitfinex(),
        }
        cnt = 0
        for ex in exchanges:
            temp = []
            temp = compareDB(ex)
            if len(temp) > 0:
                for i in temp:
                    cnt+=1
                    sendMessage(ex, i)
            else:
                pass
        print('%s - %d new pair(s)'%(now.strftime('%Y-%m-%d %H:%M:%S'), cnt))
        time.sleep(15)

    conn.close()

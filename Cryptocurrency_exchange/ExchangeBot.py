import ExchangeBotApi
import ExchangeCrawler as crawl
import pymysql
import time
import datetime

def translate(text):
    return tr.translate(text)

def sendMessage(exchange, n):
    if tr.detectLang(notiExchange[exchange][n][title]) != 'ko':
        tg.sendPlain('[%s] 거래소 공지\n<a href="%s">%s</a>'%(exchange, notiExchange[exchange][n][url], notiExchange[exchange][n][title]))
    else:
        tg.sendPlain('[%s] 거래소 공지\n<a href="%s">%s</a>'%(exchange, notiExchange[exchange][n][url], notiExchange[exchange][n][title]))

def compareDB(ex):
    new = []
    for i in range(len(notiExchange[ex])):
        sql = "SELECT title from "+ex+" where title = %s"
        if curs.execute(sql, (notiExchange[ex][i][title])) > 0:
            pass
        else:
            new.append(i)
            sql = "INSERT INTO "+ex+" (title, url) VALUES (%s, %s)"
            curs.execute(sql, (notiExchange[ex][i][title], notiExchange[ex][i][url]))
            conn.commit()
    if len(new) == 0:
        pass
        #print('['+ex+'] All data is up-to-date')
    else:
        print('['+ex+'] New %d Notification... '%(len(new)))
    return new

if __name__ == "__main__":
    conn = pymysql.connect(host='localhost', user='root', password='yewon0527', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()

    # SQL문 실행
    sql = "USE coin"
    curs.execute(sql)
    while(True):
        now = datetime.datetime.now()
        tg = ExchangeBotApi.TelegramBot()
        tr = ExchangeBotApi.GoogleTrans()

        title = 0
        url = 1

        upbit = 'Upbit'
        binance = 'Binance'
        bitmex = 'Bitmex'
        bitfinex = 'Bitfinex'
        bithumb = 'Bithumb'
        bittrex = 'Bittrex'

        notiExchange = {
                        upbit: crawl.upbit(),
                        binance: crawl.binance(),
                        bitmex: crawl.bitmex(),
                        bitfinex: crawl.bitfinex(),
                        bithumb: crawl.bithumb(),
                        bittrex: crawl.bittrex()
                        }

        cnt = 0
        for ex in list(notiExchange.keys()):
            temp = []
            temp = compareDB(ex)
            if len(temp) > 0:
                for i in temp:
                    cnt+=1
                    sendMessage(ex, i)
            else:
                pass
        print('%s - %d new update(s)'%(now.strftime('%Y-%m-%d %H:%M:%S'), cnt))
        time.sleep(0.5)

    conn.close()

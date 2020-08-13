import TwitterBotApi
import json
import pymysql
import time

def translate(text):
    return tr.translate(text)

def sendMessage(i):
    if twitter[i][3] != 'ko':
        try:
            tg.sendPlain('[Twitter]\n'+'@%s\n%s'%(twitter[i][1], translate(twitter[i][2])))
        except:
            tg.sendPlain('[Twitter]\n'+'@%s\n%s'%(twitter[i][1], twitter[i][2]))
    else:
        tg.sendPlain('[Twitter]\n'+'@%s\n%s'%(twitter[i][1], twitter[i][2]))

def compareDB():
    # 데이터베이스명은 coin
    # 테이블명은 twitter
    # 항목 id(int), name(str), tweet(str), lang(str)
    # 실행전 생성 해야함.
    new = []
    for i in range(len(twitter)):
        sql = "SELECT id from twitter where id = %s"
        if curs.execute(sql, (twitter[i][0])) > 0:
            pass
        else:
            new.append(i)
            sql = "INSERT INTO twitter (id, name, tweet, lang) VALUES (%s, %s, %s, %s)"
            curs.execute(sql, (twitter[i][0], twitter[i][1], twitter[i][2], twitter[i][3]))
            conn.commit()
    if len(new) == 0:
        print('[Twitter] All data is up-to-date')
    else:
        print('[Twitter] New %d Notification... '%(len(new)))
    return new


if __name__ == "__main__":
    # Mysql 접속 정보
    mysqlhost = 'localhost'
    mysqluser = 'root'
    mysqlpw = 'PASSWORD'

    while(True):
        tg = TwitterBotApi.TelegramBot()
        tr = TwitterBotApi.GoogleTrans()
        tw = TwitterBotApi.Twitter()

        while(True):
            try:
                tweets = tw.homeTimeline()
            except:
                print('Rate Limit')
                sleep(60) # rate limit 시 1분 대기
            else:
                break
        twitter = []
        for i in range(len(tweets)):
            twitter.append([tweets[i]._json['id'], tweets[i]._json['user']['screen_name'],tweets[i]._json['full_text'], tweets[i]._json['lang']])

        conn = pymysql.connect(host=mysqlhost, user=mysqluser, password=mysqlpw, charset='utf8')

        curs = conn.cursor()
        sql = "USE coin" # 데이터베이스명
        curs.execute(sql)

        temp = compareDB()
        if len(temp) > 0:
            for i in temp:
                sendMessage(i)
        else:
            pass

        conn.close()
        time.sleep(60) # 더 줄일 수 있지만, Twitter Rate limit이 엄격함.

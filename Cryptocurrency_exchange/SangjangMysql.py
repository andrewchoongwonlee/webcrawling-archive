import pymysql

def createTable(name):
    sql = "CREATE TABLE " + name + "(pair VARCHAR(20) NOT NULL, base VARCHAR(20) NOT NULL, quote VARCHAR(20) NOT NULL)"
    curs.execute(sql)

conn = pymysql.connect(host='localhost', user='root', password='yewon0527', charset='utf8')
curs = conn.cursor()


sql = "CREATE DATABASE pair"
curs.execute(sql)

sql = "USE pair"
curs.execute(sql)
#
createTable('bitfinex')
createTable('bittrex')
createTable('bit_z')
createTable('binance')
createTable('gdax')
createTable('hadax')
createTable('huobi')
createTable('hitbtc')
createTable('kucoin')
createTable('bithumb')
createTable('upbit')
createTable('gopax')

# sql = "SET collation_connection = utf8_general_ci"
# curs.execute(sql)
# sql = "USE coin"
# curs.execute(sql)
# sql = "ALTER DATABASE coin CHARACTER SET utf8 COLLATE utf8_general_ci"
# curs.execute(sql)
# sql = "ALTER TABLE Upbit CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
# curs.execute(sql)
# sql = "ALTER TABLE Bitmex CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
# curs.execute(sql)
# sql = "ALTER TABLE Bitfinex CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
# curs.execute(sql)
# sql = "ALTER TABLE Binance CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
# curs.execute(sql)
# sql = "ALTER TABLE Bithumb CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
# curs.execute(sql)
# sql = "ALTER TABLE Bittrex CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
# curs.execute(sql)

#sql = "CREATE TABLE twitter (id VARCHAR(200) NOT NULL, name VARCHAR(200) NOT NULL, tweet VARCHAR(1000) NOT NULL, lang VARCHAR(10) NOT NULL)"
#curs.execute(sql)

conn.close()

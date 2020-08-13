import pymysql

def createTable(name):
    sql = "CREATE TABLE " + name + "(title VARCHAR(1000) NOT NULL, url VARCHAR(1000) NOT NULL)"
    curs.execute(sql)

def init():
    sql = "CREATE DATABASE exchange"
    curs.execute(sql)
    sql = "USE exchange"
    curs.execute(sql)

conn = pymysql.connect(host='localhost', user='root', password='yewon0527', charset='utf8')
curs = conn.cursor()

sql = "CREATE DATABASE exchange"
curs.execute(sql)
sql = "USE exchange"
curs.execute(sql)
createTable('upbit')
createTable('bitmex')
# createTable('Bitfinex')
createTable('bithumb')
createTable('binance')
createTable('bittrex')

sql = "SET collation_connection = utf8_general_ci"
curs.execute(sql)
sql = "USE coin"
curs.execute(sql)
sql = "ALTER DATABASE coin CHARACTER SET utf8 COLLATE utf8_general_ci"
curs.execute(sql)
sql = "ALTER TABLE Upbit CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
curs.execute(sql)
sql = "ALTER TABLE Bitmex CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
curs.execute(sql)
sql = "ALTER TABLE Bitfinex CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
curs.execute(sql)
sql = "ALTER TABLE Binance CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
curs.execute(sql)
sql = "ALTER TABLE Bithumb CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
curs.execute(sql)
sql = "ALTER TABLE Bittrex CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci"
curs.execute(sql)

#sql = "CREATE TABLE twitter (id VARCHAR(200) NOT NULL, name VARCHAR(200) NOT NULL, tweet VARCHAR(1000) NOT NULL, lang VARCHAR(10) NOT NULL)"
#curs.execute(sql)

conn.close()

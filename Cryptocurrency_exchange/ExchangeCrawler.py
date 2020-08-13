import requests
from bs4 import BeautifulSoup
import os
import time
import json


def getUrl(atag):
    tempList = []
    for l in atag:
        links = BeautifulSoup(str(l), 'html.parser')
        if list(links.a['href'])[0:3] == ['/','a','d']:
            pass
        else:
             tempList.append(links.a['href'])
    return tempList

def upbit():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    upbitNotice = requests.get('https://api-manager.upbit.com/api/v1/notices/')
    upbitNoticeUrl = 'https://www.upbit.com/service_center/notice?id='
    upbitNoticeJson = json.loads(upbitNotice.text)
    if upbitNoticeJson['success']:
        upbitNoticeTemp = upbitNoticeJson['data']['list']
        upbitLen = len(upbitNoticeTemp)
        upbitNoticeList = []

        #upbit [title, url, date]
        for i in range(upbitLen):
            upbitNoticeList.append([upbitNoticeTemp[i]['title'], upbitNoticeUrl+str(upbitNoticeTemp[i]['id']), upbitNoticeTemp[i]['created_at']])
    else:
        print('Api error')

    return upbitNoticeList

def binance():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    binanceUrl = 'https://support.binance.com/hc/en-us'
    binance = requests.get(binanceUrl)
    binanceHtml = binance.text
    binanceParse = BeautifulSoup(binanceHtml, 'html.parser')
    NoticeLinkTemp = binanceParse.select('body > main > div > section.section.knowledge-base > section > ul > li:nth-of-type(1) > a')
    for l in NoticeLinkTemp:
        links = BeautifulSoup(str(l), 'html.parser')
        if list(links.a['href'])[0:3] == ['/','a','d']:
            pass
        else:
            binanceNoticeLink = 'https://support.binance.com'+ links.a['href']

    binanceNoticeHtml = requests.get(binanceNoticeLink).text
    binanceNoticeParse = BeautifulSoup(binanceNoticeHtml, 'html.parser')
    binanceNewListing = binanceNoticeParse.select('body > main > div.container > div > div > div > section:nth-of-type(1) > ul > li')
    binanceNotice = binanceNoticeParse.select('body > main > div.container > div > div > div > section:nth-of-type(2) > ul > li')

    binanceNewListingUrl = getUrl(binanceNewListing)
    binanceNoticeUrl = getUrl(binanceNotice)
    binanceNewListingList = []
    binanceNoticeList = []

    # binance [title, url]
    for i in range(len(binanceNewListing)):
        binanceNewListingList.append([binanceNewListing[i].text[1:-1],'https://support.binance.com/'+str(binanceNewListingUrl[i])])
    for i in range(len(binanceNotice)):
        binanceNoticeList.append([binanceNotice[i].text[1:-1],'https://support.binance.com/'+str(binanceNoticeUrl[i])])
    return binanceNewListingList+ binanceNoticeList

def bitmex():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    bitmexUrl = 'https://blog.bitmex.com/?lang=ko_kr'
    bitmex = requests.get(bitmexUrl)
    bitmexHtml = bitmex.text
    bitmexParse = BeautifulSoup(bitmexHtml, 'html.parser')

    bitmexNotice = bitmexParse.select('article > header > h1 > a')
    bitmexNoticeTime = bitmexParse.select('article > header > div > span.posted-on > a > time.entry-date.published')
    bitmexNoticeUrl = getUrl(bitmexNotice)

    bitmexNoticeList = []
    # bitmex [title, url, date]
    for i in range(len(bitmexNotice)):
        bitmexNoticeList.append([str(bitmexNotice[i]).split('rel=\"bookmark\">')[1].split('</a>')[0], bitmexNoticeUrl[i], str(bitmexNoticeTime[i]).split('datetime=\"')[1].split('\">')[0]])
    # print(bitmexNoticeList)
    return bitmexNoticeList

def bitfinex():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    bitfinexUrl = 'https://www.bitfinex.com/posts'
    bitfinex = requests.get(bitfinexUrl)
    bitfinexHtml = bitfinex.text
    bitfinexParse = BeautifulSoup(bitfinexHtml, 'html.parser')

    bitfinexNotice = bitfinexParse.select('#posts-page > div > div > div > h5 > a')
    #print(bitfinexNotice)
    bitfinexNoticeUrl = getUrl(bitfinexNotice)
    bitfinexNoticeList = []
    #bitfinex [title, url]
    for i in range(len(bitfinexNotice)):
        bitfinexNoticeList.append([bitfinexNotice[i].text.split("\n        ")[1].split("\n      ")[0],'https://www.bitfinex.com' + str(bitfinexNoticeUrl[i])])
    # print(bitfinexNoticeList)
    return bitfinexNoticeList

def bithumb():
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        bithumbUrl = 'http://bithumb.cafe/notice'
        bithumb = requests.get(bithumbUrl , headers = header)
        bithumbHtml = bithumb.text
        bithumbParse = BeautifulSoup(bithumbHtml, 'html.parser')
        bithumbNotice = bithumbParse.select('#primary-fullwidth > article > div.entry-thumb > a')
        bithumbNoticeUrl = getUrl(bithumbNotice)
        bithumbNoticeList = []
        for i in range(len(bithumbNotice)):
            bithumbNoticeList.append([bithumbNotice[i].img['alt'], bithumbNoticeUrl[i]])

        if len(bithumbNoticeList) != 0:
            return bithumbNoticeList
        else:
            print('Bithumb Crawl Error (website changed)')
            return []
    except:
        print('Bithumb Crawl Error (module error)')


def bittrex():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    bittrexUrl = 'https://support.bittrex.com/hc/en-us'
    bittrex = requests.get(bittrexUrl , headers = header)
    bittrexHtml = bittrex.text
    bittrexParse = BeautifulSoup(bittrexHtml, 'html.parser')
    # print(bittrexParse)
    bittrexTitle = bittrexParse.findAll('a', attrs={'class':'section__title-link'})
    # print(bittrexTitle[0].text)

    bittrexs = bittrexParse.findAll('ul', attrs={'class':'article-list'})
    bittrexNoticeList = []
    linksTemp = []
    titlesTemp = []
    for i in range(len(bittrexs)):
        sub = bittrexs[i].findAll('a')

        # print(bittrexTitle[i].text)
        temp = getUrl(sub)
        for l in temp:
            linksTemp.append(l)
        titleTemp = []
        for j in range(len(sub)):
            titleTemp.append(sub[j].text)
        for s in titleTemp:
            titlesTemp.append(s)

    for i in range(len(linksTemp)):
        bittrexNoticeList.append([titlesTemp[i], 'https://support.bittrex.com/' + str(linksTemp[i])])
    return bittrexNoticeList

# if __name__ == "__main__":
#     notice = {'upbit':upbit(), 'binance':binance(), 'bitmex':bitmex(), 'bitfinex':bitfinex(), 'bithumb':bithumb()}
#     print(notice)

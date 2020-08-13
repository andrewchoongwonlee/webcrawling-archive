import requests
from bs4 import BeautifulSoup as bs
from datetime import date
import xlwt
from tqdm import tqdm
from multiprocessing import Pool, Manager

def getPageList(url, page):
    searchParams = {
    'sort' : '0',
    'rdonastatus':'4',
    'page': str(page)
    }
    r = requests.get(url, params=searchParams)
    rhtml = bs(r.text, 'html.parser')
    pagelist = rhtml.find('ul', {'class': 'result_lst_area'})
    pageUrlList = [listurl.find('a').get('href') for listurl in pagelist.findAll('p', {'class' : 'tit'})]

    return pageUrlList

def getDetailDate(startDate, endDate):
    startDateStrip = [int(item) for item in startDate.split('.')]
    endDateStrip = [int(item) for item in endDate.split('.')]

    d0 = date(startDateStrip[0], startDateStrip[1], startDateStrip[2])
    d1 = date(endDateStrip[0], endDateStrip[1], endDateStrip[2])
    delta = d1 - d0
    term = delta.days

    return [startDateStrip[0], endDateStrip[0], term]

def getDetail(url):
    global data
    global fail

    try:
        r = requests.get(url)
        rhtml = bs(r.text, 'html.parser')

        try:
            donation = rhtml.find('p', {'class' : 'status_num'}).find('strong').text.replace(',','')
        except:
            donation = ''
        #print(donation)

        try:
            group = rhtml.find('div', {'class' : 'group_bx'}).find('strong').text
        except:
            group = ''
        #print(group)

        try:
            categories = rhtml.find('a', {'class' : 'theme'}).text.split(' >')
            largeCat = categories[0]
            try:
                smallCat = categories[1]
            except:
                smallCat = ''
        except:
            categories = ''
            largeCat = ''
            smallCat = ''
        #print(largeCat, smallCat)

        try:
            title = rhtml.find('h3', {'class' : 'tit'}).text
        except:
            title = ''
        #print(title)

        try:
            content = rhtml.find('ul', {'class' : 'intro_lst' }).text
        except:
            content = ''
        #print(content)

        try:
            dates = ''.join(rhtml.find('div', {'class' : 'term_area' }).find('strong').text.split()).split('~')
            #print(dates)
        except:
            dates = ''

        try:
            startDate = dates[0]
        except:
            startDate = ''

        try:    
            endDate = dates[1]
        except:
            endDate = ''

        try:
            detailDate = getDetailDate(startDate, endDate)

            startYear = detailDate[0]
            endYear = detailDate[1]
            term = detailDate[2]
        except:
            startYear = ''
            endYear = ''
            term = ''

        if int(endYear) >= 2015 and int(endYear) <= 2018:
            #print([group, donation, largeCat, smallCat, title, content, startDate, endDate, term, startYear, endYear])
            data.append([group, donation, largeCat, smallCat, title, content, startDate, endDate, term, startYear, endYear])

    except:
        fail.append(url)

def export_fail(fail):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    i = -1
    for l in tqdm(fail):
        i += 1
        sheet1.write(i, 0, l)
    
    book.save("해피빈_실패"+".xls")

def export(data):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    sheet1.write(0, 0, "기관")
    sheet1.write(0, 1, "모금액")
    sheet1.write(0, 2, "대분류")
    sheet1.write(0, 3, "소분류")
    sheet1.write(0, 4, "모금함 제목")
    sheet1.write(0, 5, "모금함 내용")
    sheet1.write(0, 6, "모금 시작일")
    sheet1.write(0, 7, "모금 종료일")
    sheet1.write(0, 8, "모금 기간")
    sheet1.write(0, 9, "모금 시작년도")
    sheet1.write(0, 10, "모금 종료년도")
    i = 0
    for l in tqdm(data):
        i = i+1
        sheet1.write(i, 0, l[0])
        sheet1.write(i, 1, l[1])
        sheet1.write(i, 2, l[2])
        sheet1.write(i, 3, l[3])
        sheet1.write(i, 4, l[4])
        sheet1.write(i, 5, l[5])
        sheet1.write(i, 6, l[6])
        sheet1.write(i, 7, l[7])
        sheet1.write(i, 8, l[8])
        sheet1.write(i, 9, l[9])
        sheet1.write(i, 10, l[10])

    book.save("해피빈"+".xls")

if __name__ ==  "__main__":
    manager = Manager()
    data = manager.list()
    # data = []
    fail = manager.list()


    mainUrl = 'https://happybean.naver.com/happybeansearch/RaiseDonationSearch.nhn'

    endYear = 2019
    i = 1
    for i in tqdm(range(3500)):
        urlList = getPageList(mainUrl, i)
        pool = Pool(processes=8)
        pool.map(getDetail, urlList)
        pool.close()
        pool.join()
        i += 1

    export(data)
    export_fail(fail)

    #getDetail('https://happybean.naver.com/donations/H000000109415?p=p&s=rsch')

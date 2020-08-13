import requests
from bs4 import BeautifulSoup
import re
from tkinter import *
from functools import partial
from multiprocessing import Pool, Manager, freeze_support
import threading
import time
import xlwt
from datetime import date


TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def session(id, pw):    
    global location
    global typeSearch
    global sess
    global my_id
    global my_pw
    global login_btn
    global location_choose
    global type_choose
    global app



    LOGIN_INFO = {
        'resid' : id.get(),
        'respass' : pw.get()
    }
    with requests.Session() as s:
        s.post('https://www.ggi.co.kr/login/ggi_login.asp', data=LOGIN_INFO)
    try:
        u = s.get('http://www.ggi.co.kr/member/myCash.asp')
        u.encoding='euc-kr'
        u = u.text
        u2= BeautifulSoup(u,'html.parser')
        u3 = u2.find('a', {'href': '/charge/cash.asp'})
    except:
        u3 = None
    if u3 != None:
        sess = s
        search_btn.configure(state=NORMAL)
        my_id.configure(state=DISABLED)
        my_pw.configure(state=DISABLED)
        login_btn.configure(state=DISABLED)
        location_choose.configure(state=NORMAL)
        type_choose.configure(state=NORMAL)
        Label(app, text='위의 조건 선택 후 검색').grid(row=6, columnspan=5, sticky=E+W)
        app.update()
    else:
        Label(app, text='로그인 실패').grid(row=6, columnspan=5, sticky=E+W)
        app.update
    


def search(typeSearch, location):
    global data
    global sess
    global search_btn
    global search_btn2
    global app
    global excel_btn


    search_btn.configure(state=DISABLED)
    excel_btn.configure(state=DISABLED)
    app.update()
    typeSearch = typeSearch.get()
    location = location.get()
    do = '09'
    if location == '서울':
        do = '09'
    elif location == '경기':
        do = '02'
    else:
        do = '11'

    total_list=[]
    if typeSearch == '진행':
        html = sess.get('http://www.ggi.co.kr/search/sojae_search_query_new.asp?resChgPage=1&pgesize=5000&Newuse=11&resTotGamAmt1=20&resTotGamAmt2=999999&viewchk=N&resSiDo='+ do)
        html.encoding='euc-kr'
        html = html.text

        soup= BeautifulSoup(html,'html.parser')

        links = soup.findAll('a' ,{'class':'list_link'})
        sagun = soup.findAll('span', id=lambda x: x and x.startswith('read_'))

        name = [''.join(s.get_text().strip().split('\r\n\t\t\t\t\t\t\t\t')) for s in sagun]
        details = [(link.get('href').split('..')[-1]).split("'))")[0] for link in links]
        

        for i in range(len(links)):
            total_list.append([name[i], details[i]])
        #print(total_list)
    else:
        html = sess.get('http://www.ggi.co.kr/Wait/sojae_search.asp?resChgPage=1&intPageSize=5000&Newuse=11&resAuctionResult=%B4%EB%B1%E2&resSiDo='+do)
        html.encoding='euc-kr'
        html = html.text

        soup= BeautifulSoup(html,'html.parser')

        sagun = soup.findAll('span', id=lambda x: x and x.startswith('read_'))

        name = [''.join(s.get_text().strip().split('\r\n\t\t\t\t\t\t\t\t')) for s in sagun]

        links = soup.findAll('a' ,{'target':'pop_new'})
        #data = [[n, link.text, link.get('href').split('..')[-1]] for n in name for link in links]
        for i in range(len(name)):
            total_list.append([name[i], links[i].text, links[i].get('href').split('..')[-1]])
    data = total_list
    print(len(data))
    search_btn.configure(state=NORMAL)
    Label(app, text=str(len(data))+'개의 물건 조건 만족').grid(row=6, columnspan=5, sticky=E+W)
    search_btn2.configure(state=NORMAL)
    app.update()

def loading(total):
    global count
    global done
    global app
    global found

    while done == False:
        lodinglabel = Label(app, text='분석중...('+str(len(count))+'/'+str(total)+')')
        lodinglabel.grid(row=6, columnspan=5, sticky=E+W)
        app.update()
        time.sleep(0.5)
    Label(app, text='분석완료: '+str(len(found))+'개의 물건 추출').grid(row=6, columnspan=5, sticky=E+W)
    app.update()

def detail(ind, found, sess, tp):
    type_ = tp
    if type_ == '진행':
        name = ind[0]
        url = ind[1]
        detail = sess.get('http://www.ggi.co.kr' + url)
        detail.encoding='euc-kr'
        detail = detail.text
        soup2 = BeautifulSoup(detail, 'html.parser')
        add = soup2.find('td', {'colspan':'5', 'class':'td_1'})
        add = str(add).split('<br>')
        trades = soup2.find('td', {'id':'TRADE'})
        total = soup2.find('td', {'colspan':'2', 'align':'right', 'height':25})
        try:
            total = ''.join([n for n in total.text if n.isdigit()])
            if total == '':
                total = False
        except:
            total = False
        try:
            top_trade = ''.join([n for n in trades.text if n.isdigit()])
            if top_trade == '':
                top_trade = False
        except:
            top_trade = False
        if total == False or top_trade == False or int(total) <= int(top_trade) or int(top_trade)<200000000:
            pass
        else:
            gam = soup2.find('td' ,{'align':'RIGHT'})

            chaemoo = str(soup2.findAll('td', {'class':'td_1'})[4]).split('<')[1].replace('\t', '').replace('\r', '').replace('\n', '').split('>')[-1].replace('/', '')
            try:
                address = (add[0].split('\r\n\t\t')[-1]).split('\t\t\t\t')[-1]
            except:
                address = 'na'
            try:
                address = remove_tags(address).replace('\n', '')
            except:
                pass

            try:
                gam_jung = ''.join([n for n in gam.text if n.isdigit()])
            except:
                gam_jung = 'na'

            
            found.append([name, chaemoo, address, gam_jung, total, top_trade])
    else:
        name = ind[0]
        address = ind[1]
        url = ind[2]
        detail = sess.get('http://www.ggi.co.kr' + url)
        detail.encoding='euc-kr'
        detail = detail.text
        soup2 = BeautifulSoup(detail, 'html.parser')
        try:
            chaemoo = soup2.findAll('td', {'width':'72%'})[0].text
            if chaemoo == '':
                chaemoo = False
        except:
            chaemoo = False


        try:
            totalwon = str(soup2.find('font', {'color':'#840000'})).split('<br/>')[-1]
            trades = soup2.find('td', {'id':'TRADE'})
            total = ''.join([n for n in totalwon if n.isdigit()])
            if total == '':
                total = False
        except:
            total = False
        try:
            top_trade = ''.join([n for n in trades.text if n.isdigit()])
            if top_trade == '':
                top_trade = False
        except:
            top_trade = False
        if total == False or top_trade == False or chaemoo == False or int(total) <= int(top_trade) or int(top_trade)<200000000:
            pass
        else:
            found.append([name, chaemoo, address, total, top_trade])


    count.append('')

def export(location, type_):
    global found
    today = str(date.today())

    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")
    if type_ == '진행':
        sheet1.write(0, 0, "사건번호")
        sheet1.write(0, 1, "채무자")
        sheet1.write(0, 2, "주소")
        sheet1.write(0, 3, "감정가")
        sheet1.write(0, 4, "등기부채권총액")
        sheet1.write(0, 5, "실거래가")
        i = 0
        for l in found:
            i = i+1
            sheet1.write(i, 0, l[0])
            sheet1.write(i, 1, l[1])
            sheet1.write(i, 2, l[2])
            sheet1.write(i, 3, l[3])
            sheet1.write(i, 4, l[4])
            sheet1.write(i, 5, l[5])
    else:
        sheet1.write(0, 0, "사건번호")
        sheet1.write(0, 1, "채무자")
        sheet1.write(0, 2, "주소")
        sheet1.write(0, 3, "등기부채권총액")
        sheet1.write(0, 4, "실거래가")
        i = 0
        for l in found:
            i = i+1
            sheet1.write(i, 0, l[0])
            sheet1.write(i, 1, l[1])
            sheet1.write(i, 2, l[2])
            sheet1.write(i, 3, l[3])
            sheet1.write(i, 4, l[4])

    book.save(today+'_'+type_.get()+"_"+location.get()+".xls")
    Label(app, text='엑셀 추출 완료').grid(row=6, columnspan=5, sticky=E+W)


if __name__ == '__main__':
    freeze_support()
    app = Tk()
    app.title('지지옥션 추출기')
    app.geometry('500x500')
    app.resizable(0, 0)
    Label(app, text="지지옥션 추출기").grid(row=0, column=0, columnspan=5, sticky=W+E)

    Label(app, text="아이디").grid(row=1, column=0)
    Label(app, text="비밀번호").grid(row=2, column=0)
    my_id = Entry(app)
    my_id.grid(row=1, column=1, columnspan=2)
    my_id.focus()
    my_pw = Entry(app, show="*")
    my_pw.grid(row=2, column=1, columnspan=2)
    login_btn = Button(app, text='로그인', command=partial(session, id=my_id, pw=my_pw))
    login_btn.grid(row=1, column=4, rowspan=2, sticky=N+S+E+W)

    Label(app, text="종류:").grid(row=4, column=0)
    type_option = ['진행', '예정']
    typeSearch = StringVar(app)
    typeSearch.set(type_option[0])
    type_choose = OptionMenu(app, typeSearch, *type_option)
    type_choose.grid(row=4, column=1, columnspan=2, sticky=E+W)
    type_choose.configure(state=DISABLED)
    Label(app, text="지역:").grid(row=5, column=0)
    location_option = ['서울', '경기', '인천']
    location = StringVar(app)
    location.set(location_option[0]) # default value
    location_choose = OptionMenu(app, location, *location_option)
    location_choose.grid(row=5, column=1, columnspan=2, sticky=E+W)
    location_choose.configure(state=DISABLED)
    search_btn = Button(app, text='검색', command=partial(search, location=location, typeSearch=typeSearch))
    search_btn.grid(row=4, column=4, rowspan=2, sticky=N+S+E+W)
    search_btn.configure(state=DISABLED)
    Label(app, text='지지옥션 로그인').grid(row=6, columnspan=5, sticky=E+W)

    def hmm():
        global done
        global count
        global found
        global search_btn
        global location_choose
        global type_choose
        global excel_btn

        tp = typeSearch.get()
        temp = data
        manager = Manager()
        found = manager.list()
        count = manager.list()

        pool = Pool(processes=16)
        done = False
        m = threading.Thread(target=partial(loading, total=len(temp)))
        m.start()
        pool.map(partial(detail, found=found, sess=sess, tp=tp), temp)
        done = True
        m.join()
        pool.close()
        pool.join()
        search_btn.configure(state=NORMAL)
        location_choose.configure(state=NORMAL)
        type_choose.configure(state=NORMAL)
        excel_btn.configure(state=NORMAL)
        

    def newthread():
        global search_btn2
        global search_btn
        global t
        global location_choose
        global type_choose

        search_btn2.configure(state=DISABLED)
        search_btn.configure(state=DISABLED)
        location_choose.configure(state=DISABLED)
        type_choose.configure(state=DISABLED)
        t = threading.Thread(target=hmm)
        t.start()
        
    search_btn2 = Button(app, text='분석', command=partial(app.after, 100, newthread))
    search_btn2.grid(row=8, columnspan=2, sticky=N+E+S+W)
    search_btn2.configure(state=DISABLED)
    excel_btn = Button(app, text='엑셀로 내보내기', command=partial(export, location=location, type_=typeSearch))
    excel_btn.grid(row=8, columnspan=3, column=2, sticky=N+E+S+W)
    excel_btn.configure(state=DISABLED)
    app.mainloop()
import cv2
import requests
from selenium import webdriver
import time
import os
from multiprocessing import Pool, Manager, freeze_support
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import uuid
from bs4 import BeautifulSoup as bs
from tkinter import *
import threading
import subprocess

# 팝플레이어 자동실행
def openURL(url):
    with open(os.getcwd() + '/config/potplayer.txt') as f:
        path = f.readlines()
    path = [x.strip() for x in path] 
    p = subprocess.Popen([path[0],url])

def get_mac():
    mac_address = ''
    mac_address +=  (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
    for ele in range(0,8*6,8)][::-1])) 
    return mac_address

def chromedriverInit():
    options = webdriver.ChromeOptions()
    options.add_argument('headless') # headless 웹드라이버 구현
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(os.getcwd() + '/webdriver/win/chromedriver', options=options)
    driver.get('http://www.full.co.kr/member/login')
    driver.implicitly_wait(3)
    return driver

def get_approved():
    hp = requests.get('https://sites.google.com/view/ramten/').text
    hpParse = bs(hp, 'html.parser')
    texts = hpParse.findAll('p')
    approvedIds = [str(id.contents[0])[2:] for id in texts if str(id.contents[0])[:2] == "+ "]
    temp = []
    for c in approvedIds:
        try:
            temp.append([c.split(' - ')[0],c.split(' - ')[1]])
        except:
            pass
    return temp

def login(event, driver, mac, id, pw):
    global app
    global my_id
    global my_pw
    global login_btn
    global cookies
    global searchLabel
    global search_id
    global search_btn
    global search_btn2
    global loginStat

    if driver.current_url != 'http://www.full.co.kr/member/login':
        driver.get('http://www.full.co.kr/member/login')
        driver.implicitly_wait(3)


    id = id.get()
    pw = pw.get()

    driver.find_element_by_class_name("input_id").send_keys(id)
    driver.find_element_by_class_name("input_pw").send_keys(pw)
    driver.implicitly_wait(3)

    approved = get_approved()
    if [id, mac] in approved:
        Label(app, text="아이디 허용",background="black", foreground="blue").grid(row=3, columnspan=5, sticky=E+W)
        app.update()
        driver.find_element_by_xpath('//*[@id="formLogin"]/div/div/fieldset/input[3]').click()
        driver.implicitly_wait(3)
        time.sleep(2)
        if driver.current_url == 'http://www.full.co.kr/member/loginRequest/':
            Label(app, text="풀티비 로그인 실패",background="black", foreground="red").grid(row=3, columnspan=5, sticky=E+W)
            app.update()
        else:
            Label(app, text="%s 풀티비 로그인 성공"%(id),background="black", foreground="blue").grid(row=3, columnspan=5, sticky=E+W)
            app.update()
            cookies = driver.get_cookies()
            login_btn.configure(state=DISABLED)
            my_id.configure(state=DISABLED)
            my_pw.configure(state=DISABLED)
            searchLabel.configure(state=NORMAL)
            search_id.configure(state=NORMAL)
            search_id.focus()
            search_btn.configure(state=NORMAL)
    else:
        Label(app, text="사용가능한 아이디가 아닙니다"%(id),background="black", foreground="blue").grid(row=3, columnspan=5, sticky=E+W)
        app.update()

def isLive(event, cookies, search_id):
    global data
    global app
    global my_id
    global my_pw
    global login_btn
    global search_btn
    
    search_btn.configure(state=DISABLED)
    Label(app, text="검색중...",background="black", foreground="white").grid(row=5, columnspan=5, sticky=E+W)
    app.update()
    search_id = search_id.get()
    try:
        with requests.Session() as s:
            for cookie in cookies:
                s.cookies.set(cookie['name'], cookie['value'])

        a = s.post('http://api.full.co.kr/live', data={'wvJU0v*HEDv!':'webPc' ,'Z2er0YyevFK6lmz': '1.0.0', 'K2zi0VyorAUH!*9UArgz': 300}).json()
        lives = {}
        for i in a['list']:
            lives[i['userId']] = [i['code'], i['sizeWidth'], i['storage']]
        if search_id in lives.keys():
            Label(app, text="%s님은 방송중입니다."%(search_id),background="black", foreground="blue").grid(row=5, columnspan=5, sticky=E+W)
            data = lives[search_id]
            search_btn2.grid(row=6, columnspan=5, sticky=E+W)
            search_btn2.configure(background="black", foreground="white")
            search_btn.configure(state=NORMAL)
            app.update()
        else:
            Label(app, text="%s님은 방송중이 아닙니다"%(search_id),background="black", foreground="red").grid(row=5, columnspan=5, sticky=E+W)
            search_btn.configure(state=NORMAL)
            app.update()
    except:
        Label(app, text="세션 만료. 다시 로그인 해주세요",background="black", foreground="red").grid(row=5, columnspan=5, sticky=E+W)
        login_btn.configure(state=NORMAL)
        my_id.configure(state=NORMAL)
        my_pw.configure(state=NORMAL)
        search_id.configure(state=DISABLED)
        search_btn.configure(state=DISABLED)
        searchLabel.configure(state=DISABLED)
        app.update()



def verifyRTMP(c, found, url_string):
    cap = cv2.VideoCapture()
    url = 'rtmp://streaming'+ c[0] +'.neofuture.kr:1935/neofuture_live0' + c[1] + url_string
    try:
        status = cap.open(url)
    except:
        pass
    else:
        if status:
            found.append(url)
def loading():
    global complete
    while complete == False:
        Label(app, text='검색중 /',background="black", foreground="white").grid(row=7, columnspan=5, sticky=E+W)
        app.update()
        time.sleep(0.25)
        Label(app, text='검색중 -',background="black", foreground="white").grid(row=7, columnspan=5, sticky=E+W)
        app.update()
        time.sleep(0.25)
        Label(app, text='검색중 \\',background="black", foreground="white").grid(row=7, columnspan=5, sticky=E+W)
        app.update()
        time.sleep(0.25)

if __name__ == "__main__":
    freeze_support()
    loginStat = False
    data = False
    cookies = ''
    driver = chromedriverInit()
    mac = get_mac()
    #mac = '00:1a:7d:da:71:03'

    app = Tk()
    app.configure(background='black')
    app.title('풀티비 검색기')
    app.geometry('246x260')
    #app.resizable(0, 0)

    Label(app, text="%s 에서 접속"%(mac),background="black", foreground="white").grid(row=0, columnspan=5)
    Label(app, text="아이디",background="black", foreground="white").grid(row=1, column=0)
    Label(app, text="비밀번호",background="black", foreground="white").grid(row=2, column=0)
    Label(app, text=" ",background="black", foreground="white").grid(row=3, columnspan=5)
    my_id = Entry(app)
    my_id.grid(row=1, column=1, columnspan=2)
    my_id.focus()
    my_pw = Entry(app, show="*")
    my_pw.grid(row=2, column=1, columnspan=2)
    login_btn = Button(app, text='로그인', command=partial(login, id=my_id, pw=my_pw, driver=driver, mac=mac, event=None))
    login_btn.grid(row=1, column=4, rowspan=2, sticky=N+S)
    login_btn.configure(background="black", foreground="white")
    searchLabel = Label(app, text="ID 검색", state=DISABLED, background="black", foreground="white")
    searchLabel.grid(row=4, column=0)
    search_id = Entry(app, state=DISABLED)
    search_id.grid(row=4, column=1, columnspan=2)
    search_btn = Button(app, text='검색', command=partial(isLive, search_id=search_id, cookies=cookies, event=None))
    search_btn.grid(row=4, column=4, sticky=E+W)
    search_btn.configure(state=DISABLED,background="black", foreground="white")
    my_pw.bind("<Return>", partial(login, id=my_id, pw=my_pw, driver=driver, mac=mac))
    search_id.bind("<Return>", partial(isLive, search_id=search_id, cookies=cookies))
    
    def rtmp():
        global search_btn2
        global complete
        global pool
        global found

        complete=False
        search_btn2.configure(state=DISABLED)
        search_btn.configure(state=DISABLED)
        manager = Manager()
        curr = time.time()
        found = manager.list()

        process_num = 32
        a = ['4','5','6','9']
        b = [str(i) for i in range(1,9)]
        c = [[i,j] for i in a for j in b]
        res = 'h'

        if data[1] == 1280:
            res = 'h'
        elif data[1] == 640:
            res = 'n'
        elif data[1] == 540:
            res = 'n'
        elif data[1] == 360:
            res = 'n'        
        elif data[1] == 854:
            res = 'm'
            
        url_string = res + '/?authkey=/'+ data[2] +'/' + data[0]
        def abortable_worker(func, *args, **kwargs):
            timeout = kwargs.get('timeout', None)
            p = ThreadPool(1)
            res = p.apply_async(func, args=args)
            try:
                out = res.get(timeout)  # Wait timeout seconds for func to complete.
                return out
            except multiprocessing.TimeoutError:
                print("Aborting due to timeout")
                p.terminate()
                raise



        pool = Pool(processes=process_num)


        #pool.map(partial(verifyRTMP, found=found, url_string=url_string), c)

        for f in c:
            worker = partial(verifyRTMP, found=found, url_string=url_string)
            abortable_func = partial(abortable_worker, worker, timeout=3)
            pool.apply_async(abortable_func, args=f)
        pool.close()
        pool.join()

        url = Text(app, width=20, height=4)
        url.grid(row=8, columnspan=5, sticky=E+W)
        complete = True
        app.update()
        time.sleep(0.75)
        Label(app, text='검증완료(%.2fs)'%(time.time() - curr),background="black", foreground="white").grid(row=7, columnspan=5, sticky=E+W)
        app.update()
        if len(found) > 0:
            url.insert(1.0, found[0])
            watchBtn = Button(app, text="실시간 보기 (팟플레이어)", command=partial(openURL, url=found[0]))     
            watchBtn.grid(row=9, columnspan=5, sticky=E+W)
            watchBtn.configure(background="black", foreground="white")
        else:
            url.insert(1.0, "스트리밍 주소를 찾지 못했습니다.")
        search_btn2.configure(state=NORMAL)
        search_btn.configure(state=NORMAL)


    def newthread():
        global t
        t = threading.Thread(target=rtmp)
        t.start()
    
    search_btn2 = Button(app, text='스트리밍 주소 검색', command=partial(app.after, 100, newthread))

    app.mainloop()
    driver.close()
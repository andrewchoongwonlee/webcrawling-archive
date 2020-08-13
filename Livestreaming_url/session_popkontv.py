import os
import requests
from bs4 import BeautifulSoup as bs
import cv2
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
import time
import sys
from tkinter import *
from functools import partial
import webbrowser
import subprocess

# 팝플레이어 자동실행
def openURL(url):
    with open(os.getcwd() + '/config/potplayer.txt') as f: # potplayer.txt 파일 경로 입력
        path = f.readlines()
    path = [x.strip() for x in path] 
    p = subprocess.Popen([path[0],url]) # 프로세스에 팝플레이어 경로와, 열고자 하는 주소 필요

# 호스트 목록 읽어오기
def getHosts():
    with open(os.getcwd() + '/config/hosts.txt') as f: # hosts.txt 파일 경로 입력
        hosts = f.readlines()
    hosts = [x.strip() for x in hosts] 

    return hosts

# 크롬드라이버 객체 생성
def ChromeWebDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless') # headless 웹드라이버 구현 (안보이는)
    options.add_argument("disable-gpu") # headless 웹드라이버 구현 (안보이는)
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(os.getcwd() + '/webdriver/win/chromedriver', options=options) # 크롬드라이버 경로 -> driver 객체 생성
    driver.get('https://www.popkontv.com/sign/sign_form.asp') # 로그인 페이지 접속
    driver.implicitly_wait(3)
    return driver

# 아이디 허용목록 웹사이트로부터 파싱
def getApproved():
    hp = requests.get('https://sites.google.com/view/ramten/').text
    hpParse = bs(hp, 'html.parser')
    texts = hpParse.findAll('p')
    approvedIds = [str(id.contents[0])[2:] for id in texts if str(id.contents[0])[:2] == "> "] # > 제거
    return approvedIds

# 크롬드라이버를 이용한 로그인 구현 -> 세션 저장
def login(id, pw, idList, driver):
    global loginStat
    global app
    global my_id
    global my_pw
    global login_btn
    global searchLabel
    global search_id
    global search_btn

    if driver.current_url != 'https://www.popkontv.com/sign/sign_form.asp':
        driver.get('https://www.popkontv.com/sign/sign_form.asp') # 로그인 페이지 접근
        driver.implicitly_wait(3)

    id = id.get()
    pw = pw.get()
    
    if id not in idList:
        Label(app, text="아이디 허용되지 않음").grid(row=3, columnspan=5)
    else:
        driver.find_element_by_name("txt_id").send_keys(id) # 아이디 입력
        driver.find_element_by_name("txt_pw").send_keys(pw) # 비밀번호 입력
        driver.implicitly_wait(3)
        driver.find_element_by_xpath('//*[@id="btn_sign"]').click() # 로그인 버튼 클릭
        driver.implicitly_wait(3)
        time.sleep(2)

        # 로그인 확인
        try:
            alert = driver.switch_to.alert # alert 팝업여부 확인 -> 팝업 시 로그인 실패
        except:
            #print('%s 로그인 성공'%(id))
            loginStat = True
            Label(app, text="id: %s 팝콘티비 로그인 성공"%(id),background="black", foreground="blue").grid(row=3, columnspan=5)

            # 로그인 성공 후 로그인창 비활성화, 검색창 활성화
            login_btn.configure(state=DISABLED)
            my_id.configure(state=DISABLED)
            my_pw.configure(state=DISABLED)
            searchLabel.configure(state=NORMAL)
            search_id.configure(state=NORMAL)
            search_btn.configure(state=NORMAL)
        else:
            #print(alert.text)
            Label(app, text=alert.text, background="black", foreground="red").grid(row=3, columnspan=5)
            alert.accept()
            driver.get('https://www.popkontv.com/') # 로그인 실패시 홈페이지로 refresh
            driver.implicitly_wait(3)

# 방송중인 주소 검색
def findURL(search_id, driver, id):
    global app
    global source_string
    global hosts

    # 허용목록에 있는 아이디 재 검증
    IdCheck = getApproved()
    IdCheck = ['llee49']
    id = id.get()
    if id not in IdCheck:
        Label(app, text="허용되지 않은 아이디"%(search_id),background="black", foreground="red").grid(row=5, columnspan=5)
        return 0

    # 방송국 주소로 이동
    search_id = search_id.get()
    channel_url = 'https://www.popkontv.com/ch/?mcId=' + search_id + '&mcPartnerCode=P-00001'
    Live = False
    try:
        cookies = driver.get_cookies() # 크롬드라이버로부터 쿠키 정보 획득
        with requests.Session() as s: # Requests 모듈의 session 으로 쿠키 정보 복사
            for cookie in cookies:
                s.cookies.set(cookie['name'], cookie['value'])

            html = s.get(channel_url).text
            htmlParse = bs(html, 'html.parser')

            for btn in htmlParse.findAll('a', {'class':'ch_btn mT10'}):
                if btn.contents[0] == "시청하기": # 시청하기 버튼 찾기
                    Live = True
                    app.update()
                    Label(app, text="%s님은 현재 방송중 입니다"%(search_id),background="black", foreground="blue").grid(row=5, columnspan=5)
                    #print("현재 방송중")
                    watch_url = btn.get('href')
                    break
                
            if not Live:
                Label(app, text="현재 방송중이 아닙니다",background="black", foreground="red").grid(row=5, columnspan=5, sticky=E+W)
                #print("현재 방송중이 아닙니다")

    except: # 방송국 접속 불가 <- 존재하지 않는 채널
        #print("존재하지 않는 채널")
        Label(app, text="존재하지 않는 채널입니다" ,background="black", foreground="red").grid(row=5, columnspan=5, sticky=E+W)
    else:
        app.update()

    # 방송 중인 경우 RTMP 주소 검색
    if Live:
        cookies = driver.get_cookies()
        with requests.Session() as s:
            for cookie in cookies:
                s.cookies.set(cookie['name'], cookie['value'])
            watch_html = s.get(watch_url).text
            watch_htmlParse = bs(watch_html, 'html.parser')
            num = watch_htmlParse.find('div', {'class':'js-btn-liveView'}).get('id').split('-')[-1] # 고유 숫자 가져오기
            source_string = search_id + '_P-00001_' + num

            Label(app, text="주소 파싱 완료",background="black", foreground="white").grid(row=6, columnspan=5, sticky=E+W)
            Label(app, text='검증중..',background="black", foreground="white").grid(row=7, columnspan=5, sticky=E+W)
            app.update()
            verifyRTMP(urlString=source_string, hosts=hosts) # RTMP 주소 검증

            # 이하 검색버튼 활성화지만 삭제.
            #search_btn = Button(app, text='스트리밍 주소 찾기', command=partial(verifyRTMP, urlString=source_string, hosts=hosts))
            #search_btn.grid(row=7, columnspan=5, sticky=E+W)
            #search_btn.configure(background="black", foreground="white")

# RTMP 주소 검증
# OpenCv 모듈의 VideoCapture 메소드를 이용한 RTMP 주소 검증
def verifyRTMP(hosts, urlString):
    global app
    temp = []
    cap = cv2.VideoCapture() 
    for host in hosts:
        video_url = (host + urlString)
        try:
            status = cap.open(video_url)
        except:
            pass
        else:
            if status:
                temp.append(video_url)

    url = Text(app, width=20, height=4)
    url.grid(row=8, columnspan=5, sticky=E+W)
    Label(app, text='검증완료',background="black", foreground="white").grid(row=7, columnspan=5, sticky=E+W)
    if len(temp) > 0:
        #print(temp)
        url.insert(1.0, temp[0])
        watchBtn = Button(app, text="실시간 보기", command=partial(openURL, url=temp[0]))     
        watchBtn.grid(row=9, columnspan=5, sticky=E+W)
        watchBtn.configure(background="black", foreground="white")
    else:
        url.insert(1.0, "스트리밍 주소를 찾지 못했습니다.")

        

if __name__ == "__main__":
    loginStat = False
    hosts = getHosts()
    app = Tk() # tkinter GUI 객체 생성
    app.configure(background='black')
    app.title('팝콘티비 검색기')
    app.geometry('246x255')
    app.resizable(0, 0)
   
    driver = ChromeWebDriver()
    approvedIds = getApproved()
    approvedIds = ['llee49']
    # GUI 구성요소
    Label(app, text="팝콘티비 로그인",background="black", foreground="white").grid(row=0, columnspan=5)
    Label(app, text="아이디",background="black", foreground="white").grid(row=1, column=0)
    Label(app, text="비밀번호",background="black", foreground="white").grid(row=2, column=0)
    Label(app, text=" ",background="black", foreground="white").grid(row=3, columnspan=5)
    my_id = Entry(app)
    my_id.grid(row=1, column=1, columnspan=2)
    my_pw = Entry(app, show="*")
    my_pw.grid(row=2, column=1, columnspan=2)
    login_btn = Button(app, text='로그인', command=partial(login, id=my_id, pw=my_pw, idList=approvedIds, driver=driver))
    login_btn.grid(row=1, column=4, rowspan=2, sticky=N+S)
    login_btn.configure(background="black", foreground="white")
    searchLabel = Label(app, text="ID 검색", state=DISABLED, background="black", foreground="white")
    searchLabel.grid(row=4, column=0)
    search_id = Entry(app, state=DISABLED)
    search_id.grid(row=4, column=1, columnspan=2)
    search_btn = Button(app, text='검색', command=partial(findURL, search_id=search_id, driver=driver, id=my_id))
    search_btn.grid(row=4, column=4, sticky=E+W)
    search_btn.configure(state=DISABLED,background="black", foreground="white")

    app.mainloop()
    driver.close() # 크롬드라이버 종료

# 모듈 설치 목록
# 1. requests (pip install requests) # 사용법은 공식 문서 참조
# 2. selenium (pip install selenium) # 자바스크립트를 실행해야 하기때문에 requests 만으로 불가능.
# 3. bs4 (pip install bs4) # 사용법은 공식 문서 참조
# 

## 파이썬 잘 모르신다고 하셔서 쉬운 문법과 구조로만 구성하였습니다.


from selenium import webdriver
# 코드 변경으로 사용 X
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
import urllib.parse as urlparse
import requests
from bs4 import BeautifulSoup as bs
import json
import os
import time
import threading
import sys
from multiprocessing import Pool 


def getLink(num):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'} # request 모듈에 header 추가 권장

    crawlUrl = 'http://vod.afreecatv.com/PLAYER/STATION/' + str(num)
    crawl = requests.get(crawlUrl, headers=header).text
    crawlParse = bs(crawl, 'html.parser')
    
    try:
        rawUrl = crawlParse.find('meta', property='og:video').get('content') 
    except:
        rawUrl = False
    
    try:
        bjNick = crawlParse.find('span', id='bjNick').contents[0] # BJ 닉네임
    except:
        bjNick = 'NULL'
    
    if rawUrl != False:
        parsedUrl = urlparse.urlparse(rawUrl)

        # 주소변환에 필수 정보들을 기존 url로부터 파싱
        nStationNo = urlparse.parse_qs(parsedUrl.query)['nStationNo'][0]
        nBbsNo = urlparse.parse_qs(parsedUrl.query)['nBbsNo'][0]
        nTitleNo = urlparse.parse_qs(parsedUrl.query)['nTitleNo'][0]

        # Link 주소를 알 수 있는 XML 주소로 변경
        newUrl = 'http://afbbs.afreecatv.com:8080/api/video/get_video_info.php'
        
        params = {
            'nStationNo': nStationNo,
            'nBbsNo': nBbsNo,
            'nTitleNo': nTitleNo
            }

        req = requests.get(newUrl, params=params) # 새로운 주소로 http 요청

        reqHtml = req.text
        htmlParse = bs(reqHtml, 'html.parser')

        # 비디오 정보 파싱 및 저장
        try:
            title = htmlParse.find('title').contents[0]
        except:
            title = 'NULL'
        
        try:
            date = htmlParse.find('reg_date').contents[0]
        except:
            date = 'NULL'
        
        try:
            id = htmlParse.find('bj_id').contents[0]
        except:
            id = 'NULL'

        # 파일 태그 모두 저장
        fileTags = htmlParse.findAll('file')

        links = []
        [links.append(f.contents[0]) for f in fileTags if f.get('key')] # 저장한 정보 중 유효한 태그에서 파일 주소 추출
        chats = []
        [chats.append('http://videoimg.afreecatv.com/php/ChatLoad.php?rowKey=' + f.get('key') + '_c') for f in fileTags if f.get('key')] # 파일마다 key값 추출하여 채팅 주소에 첨부
        
        data = {
            '1_no' : num,
            '2_bj': bjNick,
            '3_id': id,
            '4_date' : date,
            '5_title': title,
            '6_links': links,
            '7_chat': chats
            }

        print(data) # 콘솔에 출력하기 위함

        # 데이터 저장
        with open('db.txt', 'a', encoding='utf-8') as file:
            file.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)+'\n')

# 프로그램이 작동중임을 보여주는 loading 문구
def loading():
    global done
    while done != True:
        try:
            sys.stdout.write('\rchecking Afreeca for new VOD |')
            time.sleep(0.2)
            sys.stdout.write('\rchecking Afreeca for new VOD /')
            time.sleep(0.2)
            sys.stdout.write('\rchecking Afreeca for new VOD -')
            time.sleep(0.2)
            sys.stdout.write('\rchecking Afreeca for new VOD \\')
            time.sleep(0.2)
            sys.stdout.flush()
        except KeyboardInterrupt:
            break
    sys.stdout.flush()
    
# 메인함수
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('headless') # headless 웹드라이버 구현
    options.add_argument("disable-gpu")
    # 위 두줄 주석처리하여 크롤링 상태 확인 가능

    driver = webdriver.Chrome(os.getcwd() + '\\webdriver\\win\\chromedriver', chrome_options=options) # 크롬드라이버 path -> driver 객체 생성
    driver.get('http://vod.afreecatv.com/ALL') # VOD list 접근
    driver.implicitly_wait(3)
    nums = []
    print('webdriver ready to crawl')

    while True:
        try:
            done = False
            t = threading.Thread(target=loading)
            t.start()
            driver.get('http://vod.afreecatv.com/ALL') # VOD list 접근
            driver.implicitly_wait(3)
            driver.find_element_by_xpath('//*[@id="order"]/li[4]/a').click() # 최신순 클릭
            driver.implicitly_wait(3)
            time.sleep(1.5) # 자바스크립트가 로딩되어야 하므로 시간지연이 있어야 함. 현재(1.5초) 더 줄일 수 도 있지만 webdriver을 처리하는 서버의 능력에 따라 다름
            html = driver.page_source
            soup = bs(html, 'html.parser')
            li = soup.findAll('div', attrs={'class': 'cast_box'}) # 리스트 항목 검색
            temp = []
            newNum = []
            [temp.append(int(a.contents[1].get('href').split('#')[0].split('/')[-1])) for a in li] # 동영상 고유번호 추출
            [newNum.append(num) for num in temp if num not in nums] # 새로운 영상 분류
            nums = temp
            #print(nums)
            if len(newNum) > 0: # 감지된 신규 동영상이 있는 경우에만 실행
                done = True
                pool = Pool(processes=4) # process는 많다고 빠른것이 아니다. 서버 성능에 따라 변경
                pool.map(getLink, newNum) 
                pool.close()
                pool.join()
            else:
                pass
        except KeyboardInterrupt:
            try:
                pool.close()
            except:
                pool.terminate()
                raise
            finally:
                pool.join()
                break
    driver.close()
    exit()
    
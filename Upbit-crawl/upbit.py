import socket
import os
import requests
import json
import time
from time import gmtime, strftime
from datetime import datetime
import uuid

def getMac():
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        return mac

def timeC(timestamp):
    return datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y/%m/%d %H:%M:%S')

def getJson(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    api = requests.get(url, headers = header)
    api_json = api.json()
    return api_json

def initialize():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    dataPath = BASE_DIR+'/data'
    if not os.path.exists(dataPath):
        os.makedirs(dataPath)

    noticeUrl = 'https://api-manager.upbit.com/api/v1/notices'
    noticeJson = getJson(noticeUrl)

    noticeData = {}
    if noticeJson['success'] == True:
        notices = noticeJson['data']['list']
        for notice in notices:
            noticeData[notice['id']] = {
                'title': notice['title'],
                'created': notice['created_at'],
                'updated': notice['updated_at']
            }
    with open(os.path.join(BASE_DIR+'/data/notice.json'), 'w+') as outfile:
        json.dump(noticeData, outfile, indent = 4, ensure_ascii = False)

    coinUrl = 'https://s3.ap-northeast-2.amazonaws.com/crix-production/crix_master'
    coinJson = getJson(coinUrl)
    coinData = {}
    for coins in coinJson:
        if coins['exchange'] == 'UPBIT':
            coinData[coins['pair']] = {
                'base': coins['baseCurrencyCode'],
                'quote':coins['quoteCurrencyCode'],
                'trade':coins['tradeStatus'],
                'market':coins['marketState'],
                'timestamp':coins['timestamp']
            }

    with open(os.path.join(BASE_DIR+'/data/coin.json'), 'w+') as outfile:
        json.dump(coinData, outfile, indent = 4, ensure_ascii = False)

def getNotice(noticeData):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    noticeUrl = 'https://api-manager.upbit.com/api/v1/notices'
    noticeJson = getJson(noticeUrl)

    if noticeJson['success'] == True:
        notices = noticeJson['data']['list']
        for notice in notices:
            if str(notice['id']) not in noticeData.keys():
                ## 출력
                print('[' + currtime + '] 신규 공지')
                print(notice['title'])
                print('https://upbit.com/service_center/notice?id='+str(notice['id']))
                noticeData[str(notice['id'])] = {
                    'title': notice['title'],
                    'created': notice['created_at'],
                    'updated': notice['updated_at']
                }

            else:
                pass


    with open(os.path.join(BASE_DIR+'/data/notice.json'), 'w+') as outfile:
        json.dump(noticeData, outfile, indent = 4, ensure_ascii = False)

    return noticeData

def getCoin(coinData):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    coinUrl = 'https://s3.ap-northeast-2.amazonaws.com/crix-production/crix_master'
    coinJson = getJson(coinUrl)
    for coins in coinJson:
        if coins['exchange'] == 'UPBIT':
            if coins['pair'] not in coinData.keys():
                
                ## 출력
                print('[' + currtime + '] 새로운 코인쌍')
                print('코인: '+coins['pair'])
                print('거래: '+coins['tradeStatus'])
                print('마켓: '+coins['marketState'])


                coinData[coins['pair']] = {
                    'base': coins['baseCurrencyCode'],
                    'quote':coins['quoteCurrencyCode'],
                    'trade':coins['tradeStatus'],
                    'market':coins['marketState'],
                    'timestamp':coins['timestamp']
                }
                
            else:
                if (coins['tradeStatus'] != coinData[coins['pair']]['trade']) or (coins['marketState'] != coinData[coins['pair']]['market']):
                    

                    ## 출력
                    print('[' + currtime + '] 마켓 상태 변동')
                    print('코인: '+coins['pair'])
                    print('거래: '+coins['tradeStatus'])
                    print('마켓: '+coins['marketState'])
                    
                    coinData[coins['pair']]['trade'] = coins['tradeStatus']
                    coinData[coins['pair']]['market'] = coins['marketState']

                else:
                    pass
    
    with open(os.path.join(BASE_DIR+'/data/coin.json'), 'w+') as outfile:
        json.dump(coinData, outfile, indent = 4, ensure_ascii = False)

    return coinData

if __name__ == '__main__':
    #print(getMac())


    #license = input('Enter License Code: ')
    # if license = 
    currtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    #initialize()
    noticeData = json.loads(open(BASE_DIR+'/data/notice.json').read())
    coinData = json.loads(open(BASE_DIR+'/data/coin.json').read())

    print('Start Crawling. Press ctrl+c to quit')
    print('Logs will show below.')
    print('Datas will be saved in \'/data\' folder.')


    while True:
        try:
            noticeData = getNotice(noticeData)
            coinData = getCoin(coinData)
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except:
            break
    
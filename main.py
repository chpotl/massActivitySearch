import requests
import time
import datetime

API_KEY = "" #eth scan api key
def main():
    SAME_TRX_COUNT = int(input("Количество транзакций для уведомления: "))
    TIME_FRAME_SEC = int(input("Частота уведомлений (мин): "))*60
    adrList = []
    with open("address.txt") as f:
        for line in f:
            adrList.append(line.replace("\n", ""))
    while True:
        timestamp = round(time.time())
        dt = datetime.datetime.today()
        print(f'-------------- Last update: {dt.year}/{dt.month}/{dt.day} {time.strftime("%H:%M:%S", time.localtime())}  --------------')
        getTRX(adrList, timestamp-TIME_FRAME_SEC, SAME_TRX_COUNT)
        time.sleep(TIME_FRAME_SEC)


def getBlockNumber(_timestamp):
    reqLink = f'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={_timestamp}&closest=before&apikey={API_KEY}'
    return requests.get(reqLink).json()["result"]

def getTRX(_adrList, _timeatamp, _same_trx_count):
    startBlock = getBlockNumber(_timeatamp)
    jsonArr = []
    for _adr in _adrList:
        reqLink = f'https://api.etherscan.io/api?module=account&action=txlist&address={_adr}&startblock={startBlock}&endblock=99999999&sort=desc&apikey={API_KEY}'
        r = requests.get(reqLink).json()["result"]
        jsonArr+=r
    jsonArr.sort(key=lambda x: x["timeStamp"])
    toList = []
    countDict = {}
    for trx in jsonArr:
        toList.append(trx["to"])
    for el in toList:
        countDict[el] = toList.count(el)
    tmp=True
    for key, value in countDict.items():
        if value > _same_trx_count:
            print(f'ALERT {toList.count(key)} транзакциый ушло на  https://etherscan.io/address/{key}')
            tmp = False
    if tmp:
        print("Не было подозрительной активности")

if __name__ == '__main__':
    main()

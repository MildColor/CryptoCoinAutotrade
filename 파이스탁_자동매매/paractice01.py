# 업비트는 마켓코드를 통해 주문을 수행합니다. 앞서 제공한 REST API 코드를 사용해서 원화시장에서 거래가 가능한 가사화폐의 마켓코드를 파이썬 리스트로 저장해보세요.

import requests

url = "https://api.upbit.com/v1/market/all"
resp = requests.get(url)
data = resp.json() #JSON 자바스크립트 로테이션이라는 타입을 파이썬에 딕셔너리나 기본데이터 타입으로 변환

krw_tickers = []

for coin in data: 
    ticker = coin['market']     #coin is dict, 

    if ticker.startswith("KRW"):    #"KRW_BTC"
        krw_tickers.append(ticker)

print(krw_tickers)
print(len(krw_tickers))
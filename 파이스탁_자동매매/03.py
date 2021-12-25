# 업비트 마켓코드 조회하기

import pyupbit #모듈

tickers = pyupbit.get_tickers(fiat="KRW")
print(tickers)
print(len(tickers))

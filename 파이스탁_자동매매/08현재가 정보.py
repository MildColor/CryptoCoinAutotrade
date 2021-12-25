import pyupbit

price = pyupbit.get_current_price("KRW-BTC")
print(price)


#여러종목의 현재가
tickers = ["KRW-BTC", "KRW-XRP"]
price = pyupbit.get_current_price(tickers)
print(price)

#업비트 거래소의 원화 시장에서 거래되고 있는 모든 가상화페에 대한 현재가를 조회하고 이를 화면에 출력해보세요

krw_tickers = pyupbit.get_tickers(fiat="KRW")
price_krw = pyupbit.get_current_price(krw_tickers)

for k, v in price_krw.items():
    print(k, v)


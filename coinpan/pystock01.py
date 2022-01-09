import ccxt
import pprint

binance = ccxt.binance() # binance class의 객체 생성
markets = binance.load_markets() #binance를 .load markets()메소드를 이용하여 markets 를 딕셔너리 형태로 가져옴

#print(markets.keys())
#print(len(markets))

#for market in markets.keys():
#    print(market)

for market in markets.keys():
    if market.endswith("/USDT"): # 만약 문자열이 /USDT로 끝나면 그것만 print해라
        print(market)



# 현재가 조회
btc = binance.fetch_ticker("BTC/USDT") # USDT로 BTC를 사는 market ticker를 통해 해당 마켓의 정보를 가져온다.
pprint.pprint(btc)
print("현재가", btc["last"])
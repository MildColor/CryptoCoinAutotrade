from datetime import datetime
import ccxt
import pprint
import pandas as pd

# 파일로부터 apiKey, Secret 읽기
with open ("coinpan/api.txt") as f: 
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

# binance 객체 생성, default 값을 future로 
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options':{
        'defaultType':'future' 
    }
}) 

# # 매수/롱 포지션 진입, 청산
# order = binance.create_market_buy_order(
#     symbol = "BTC/USDT",
#     amount = 0.001 
# )
# print(order)

# order = binance.create_market_sell_order(
#     symbol= "BTC/USDT"
#     amount= 0.01
# )

# # 매도/숏 포지션 진입, 청산
# order = binance.create_market_sell_order(
#     symbol = "BTC/USDT",
#     amount = 0.001 
# )
# print(order)

# order = binance.create_market_buy_order(
#     symbol= "BTC/USDT"
#     amount= 0.001
# )


# Leverage 설정
markets = binance.load_markets()
symbol = "BTC/USDT"
market = binance.market(symbol)
pprint.pprint(market) # 마켓 정보

resp = binance.fapiPrivate_post_leverage({
    'symbol' : market['id'],
    'leverage' : 2,
})



#print(resp)
#binance.create_market_buy_order(symbol="BTC/USDT", amount=0.001)

'''
# 현재 포지션 정보를 얻기
balance = binance.fetch_balance()
positions = balance['info']['positions'] # print(type(positions))

for position in positions:
    if position['symbol'] == 'BTCUSDT':
         pprint.pprint(position)
'''
'''
ticker = "BTCUSDT"
def now_position(ticker):
    balance = binance.fetch_balance()
    positions = balance['info']['positions'] 

    for position in positions:
        if position['symbol'] == ticker:
            return(pprint.pprint(position))

now_position(ticker=ticker)
'''

'''
# 대기 주문(open order), 미체결된 주문 조회
open_orders = binance.fetch_open_orders(symbol="BTC/USDT")
# pprint.pprint(open_order)
for order in open_orders:
    print(order)
'''
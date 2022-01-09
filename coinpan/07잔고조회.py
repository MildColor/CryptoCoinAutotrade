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

# 선물 현재 USDT 잔고 조회, binance
balance = binance.fetch_balance(params={"type": "future"})
print(balance['USDT'])

# 선물 BTC/USDT 현재가 조회
btc = binance.fetch_ticker("BTC/USDT")
pprint.pprint(btc["last"])

# 선물 OHLCV 조회
btc_ohlcv = binance.fetch_ohlcv(symbol="BTC/USDT", timeframe='1d', since=None, limit=10)
df = pd.DataFrame(data=btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
df.set_index('datetime', inplace=True)
# print(df)

# 선물 orderbook 조회 
order_book = binance.fetch_order_book("BTC/USDT")
order_book.keys()

asks = order_book['asks'] # 매수호가 500개
bids = order_book['bids'] # 매도호가 500개

print(type(asks), len(asks), asks[0], bids[0])
# pprint.pprint(asks)
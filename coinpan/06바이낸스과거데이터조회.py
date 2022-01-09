import ccxt
import pandas as pd
import pprint


binance = ccxt.binance() # binance class의 객체 생성
btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", "1m") # [time,ohlcv]같은 2차원리스트 형태로 받게 된다.

df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume']) # 2차원리스트의 형태로 받은 것을 컬럼이름을 정해주고 dataframe으로 바꿔주는 코드
df['datetime'] = pd.to_datetime(df['datetime'], unit = 'ms') # datetime column값을 가지고 ms단위로 timestamp값을 시간타입으로 바꿔 주는것
df.set_index('datetime', inplace=True) # 시간타입으로 바뀐 값을 dataframe에 index로 설정, 원본에 대해 바로 적용

print(df)
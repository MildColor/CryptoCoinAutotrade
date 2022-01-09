import pandas as pd
import numpy as np
import ccxt


binance = ccxt.binance(config={
    'enableRateLimit': True,
    'options':{
        'defaultType':'future' 
    }
}) 

'''
# 바이낸스 api를 통해 ohlcv 가져오기

btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", "1d", limit=200) # [time,ohlcv]같은 2차원리스트 형태로 받게 된다.

df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume']) # 2차원리스트의 형태로 받은 것을 컬럼이름을 정해주고 dataframe으로 바꿔주는 코드
df['datetime'] = pd.to_datetime(df['datetime'], unit = 'ms') # datetime column값을 가지고 ms단위로 timestamp값을 시간타입으로 바꿔 주는것
df.set_index('datetime', inplace=True) # 시간타입으로 바뀐 값을 dataframe에 index로 설정, 원본에 대해 바로 적용

print(df)

'''
d = pd.read_csv("coinpan/CMEdata.csv", sep=",")
df = d.sort_values('datetime')
print(df)


df['long range'] = (df['high'] - df['low']) * 0.77
df['short range'] = (df['high'] - df['low']) * 0.06

df['long target'] = df['open'] + df['long range'].shift(1)
df['short target'] = df['open'] - df['short range'].shift(1)


fee = 0.0016

df['long ror'] = np.where(df['high'] > df['long target'],
                     df['close'] / df['long target'] - fee, 
                     1)


df['short ror'] = np.where(df['low'] < df['short target'],
                      df['short target'] / df['close'] - fee, 
                     1)

# 누적곱계산 => 누적수익률
df['long hpr'] = df['long ror'].cumprod()
df['short hpr'] = df['short ror'].cumprod()

# Draw Down 계산
df['long dd'] = (df['long hpr'].cummax() - df['long hpr']) / df['long hpr'].cummax() * 100
df['short dd'] = (df['short hpr'].cummax() - df['short hpr']) / df['short hpr'].cummax() * 100

# MDD 계산
print("MDD(%): ", df['long dd'].max())
print("MDD(%): ", df['short dd'].max())


df.to_excel("coinpan/cme_backtestingdata.xlsx")
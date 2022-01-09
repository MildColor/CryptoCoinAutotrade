import pyupbit
import ccxt
import numpy as np
import pandas as pd
import time

# upbit 
def get_upbit_ror(k):
    df = pyupbit.get_ohlcv("KRW-BTC", count=30)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0016
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)
    time.sleep(0.2)
    ror = df['ror'].cumprod()[-2]
    return ror

# binance future
def get_binance_ror(k):
    binance = ccxt.binance() 
    btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", "1d",limit=10) 

    df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume']) 
    df['datetime'] = pd.to_datetime(df['datetime'], unit = 'ms') 
    df.set_index('datetime', inplace=True) 

    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0016
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)
    time.sleep(0.2)
    ror = df['ror'].cumprod()[-2]
    return ror



ror_dict = {}
for k in np.arange(0.1, 1.0, 0.1):
    ror = get_binance_ror(k)
    ror_dict[k] = ror
    print("%.3f %f" % (k, ror))

print(ror_dict)

max_key = max(ror_dict, key=ror_dict.get)

secondmin_key = max_key - 0.05
secondmax_key = max_key + 0.05

while secondmin_key >= secondmax_key:
    ror = get_binance_ror(secondmin_key)
    secondmin_key =+ 0.01 
    print(ror, secondmin_key)



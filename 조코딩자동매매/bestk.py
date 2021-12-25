import pyupbit
import numpy as np
import time

def get_ror(k):
    df = pyupbit.get_ohlcv("KRW-BTC", count=200)
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
    ror = get_ror(k)
    ror_dict[k] = ror
    print("%.3f %f" % (k, ror))

print(ror_dict)

max_key = max(ror_dict, key=ror_dict.get)
print(max_key)

secondmin_key = max_key - 0.05
secondmax_key = max_key + 0.05
print(secondmin_key)
print(secondmax_key)

while secondmin_key >= secondmax_key:
    ror = get_ror(secondmin_key)
    secondmin_key =+ 0.01 
    print(ror, secondmin_key)



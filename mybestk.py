import pyupbit
import numpy as np
import time

def get_ror(k):
    df = pyupbit.get_ohlcv("KRW-BTC", "day", 14)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0016
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)
    time.sleep(0.2)
    ror = df['ror'].cumprod()[-2]
    return ror

def bestk():
    ror_dict = {}
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(k)
        ror_dict[k] = ror
        # print("%.3f %f" % (k, ror))
    # print(ror_dict)

    max_key = max(ror_dict, key=ror_dict.get)
    # print(max_key)

    secondmin_key = max_key - 0.05
    secondmax_key = max_key + 0.05


    count = 0
    bestk_dict = {}
    while count < 10:
        if secondmin_key <= secondmax_key:
            ror = get_ror(secondmin_key)
            bestk_dict[secondmin_key] = ror
        
            # print("%.3f %f" % (secondmin_key, ror))

        secondmin_key += 0.01 
        count += 1
    print(bestk_dict)
    
    max_key2 = max(bestk_dict, key=bestk_dict.get)
    return(max_key2)
   
mybestk = bestk()
print(mybestk)
    

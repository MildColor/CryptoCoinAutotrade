import ccxt
import numpy as np
import pandas as pd
import time
import math

symbol = "BTC/USDT"
time_interval = "1d"
limit_num = 200
# binance future
def get_binance_ror(symbol, time_interval, k, limit_num, beting_position):
    binance = ccxt.binance() 
    symbol_ohlcv = binance.fetch_ohlcv(symbol, time_interval, limit=limit_num) 

    df = pd.DataFrame(symbol_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume']) 
    df['datetime'] = pd.to_datetime(df['datetime'], unit = 'ms') 
    df.set_index('datetime', inplace=True) 
    df['range'] = (df['high'] - df['low']) * k
    fee = 0.0016

    if beting_position == "long":
        df['long target'] = df['open'] + df['range'].shift(1)
        df['long ror'] = np.where(df['high'] > df['long target'],
                     df['close'] / df['long target'] - fee, 
                     1)
        time.sleep(0.2)

        long_ror = df['long ror'].cumprod()[-2]
        return(long_ror)
    
    else:
        df['short target'] = df['open'] - df['range'].shift(1)
        df['short ror'] = np.where(df['low'] < df['short target'],
                      df['short target'] / df['close'] - fee, 
                     1)               
        time.sleep(0.2)

        short_ror = df['short ror'].cumprod()[-2]
        return(short_ror)


def best_k(symbol, time_interval, beting_position):
    ror_dict = {}
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_binance_ror(symbol, time_interval, k, limit_num, beting_position)
        ror_dict[k] = ror

    max_key = max(ror_dict, key=ror_dict.get) + 0.05
    min_key = max(ror_dict, key=ror_dict.get) - 0.05

    f_ror_dict ={}
    for m in np.arange(min_key, max_key, 0.01):
        ror = get_binance_ror(symbol, time_interval, m, limit_num, beting_position)
        f_ror_dict[m] = ror
        # print("%.3f %f" % (m, ror))

    final_k = max(f_ror_dict, key=f_ror_dict.get)
    return(final_k)

#print(get_binance_ror(symbol, time_interval, 0.5, limit_num, "long"))
#print(best_k(symbol, time_interval, "long"))
#print(best_k(symbol, time_interval, "short"))



# CME future
def get_CME_ror(k, beting_position):
    df = pd.read_csv("coinpan/CMEdata.csv", sep=",")

    df['range'] = (df['high'] - df['low']) * k
    fee = 0.0016

    if beting_position == "long":
        df['long target'] = df['open'] + df['range'].shift(1)
        df['long ror'] = np.where(df['high'] > df['long target'],
                     df['close'] / df['long target'] - fee, 
                     1)
        time.sleep(0.2)
        
        long_ror_prod = df['long ror'].cumprod()
        long_ror = long_ror_prod.iloc[-2]
        return(long_ror)
    
    else:
        df['short target'] = df['open'] - df['range'].shift(1)
        df['short ror'] = np.where(df['low'] < df['short target'],
                      df['short target'] / df['close'] - fee, 
                     1)               
        time.sleep(0.2)

        short_ror_prod = df['short ror'].cumprod()
        short_ror = short_ror_prod.iloc[-2]
        return(short_ror)


def best_CME_k(beting_position):
    ror_dict = {}
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_CME_ror(k, beting_position)
        ror_dict[k] = ror
        print(k, ror)
        
    

    max_key = max(ror_dict, key=ror_dict.get) + 0.05
    min_key = max(ror_dict, key=ror_dict.get) - 0.05

    f_ror_dict ={}
    for m in np.arange(min_key, max_key, 0.01):
        ror = get_CME_ror(m, beting_position)
        f_ror_dict[m] = ror
        #print("%.3f %f" % (m, ror))

    final_k = max(f_ror_dict, key=f_ror_dict.get)
    return(final_k)

#print(best_CME_k("long"))
#print(best_CME_k("short"))











'''
ror_dict = {}
for k in np.arange(0.1, 1.0, 0.1):
    ror = get_binance_ror(symbol, range, k)
    ror_dict[k] = ror
    print("%.3f %f" % (k, ror))

print(ror_dict)

max_key = max(ror_dict, key=ror_dict.get) + 0.05
min_key = max(ror_dict, key=ror_dict.get) - 0.05

f_ror_dict ={}
for m in np.arange(min_key, max_key, 0.01):
    ror = get_binance_ror(symbol, range, m)
    f_ror_dict[m] = ror
    print("%.3f %f" % (m, ror))

final_k = max(f_ror_dict, key=f_ror_dict.get)
print("%.2f" %final_k)
'''
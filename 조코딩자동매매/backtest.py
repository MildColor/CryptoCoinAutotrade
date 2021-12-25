import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", "minute30", count= 200)
df['range'] = (df['high'] - df['low']) * 0.18
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0016
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee, 
                     1)

# 누적곱계산 => 누적수익률
df['hpr'] = df['ror'].cumprod()
# Draw Down 계산
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
# MDD 계산
print("MDD(%): ", df['dd'].max())
df.to_excel("조코딩자동매매/backtestingdata.xlsx")
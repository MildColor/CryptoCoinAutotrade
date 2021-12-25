import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC", "day", 200)
# print(df.head())
df.to_excel("파이스탁_자동매매/btc.xlsx")
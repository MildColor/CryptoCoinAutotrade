import pyupbit

df = pyupbit.get_ohlcv(ticker="KRW-BTC",interval="day", count=10)
print(df)
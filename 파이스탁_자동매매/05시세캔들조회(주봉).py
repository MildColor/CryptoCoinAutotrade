import pyupbit

df = pyupbit.get_ohlcv(ticker="KRW-BTC",interval="week")
#df.to_excel("week_btc.xlsx") 엑셀파일로 저장
print(df)
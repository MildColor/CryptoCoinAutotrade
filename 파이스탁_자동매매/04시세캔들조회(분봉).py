import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC", "minute1")


#만약 2분몽을 얻고 싶을때(n분봉의 원리)
#pandas의 resample() 함수를 사용

df['open'].resample('3T').first()
df['high'].resample('3T').max()
df['low'].resample('3T').min()
df['close'].resample('3T').last()
df['volume'].resample('3T').sum()


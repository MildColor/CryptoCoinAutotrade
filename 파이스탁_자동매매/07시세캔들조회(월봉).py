import pyupbit
import pandas as pd

pd.options.display.float_format = "{:.1f}".format #실수값을 프린트할때 포맷을 지정할 수 있다, 소수점이하 1자리까지 프린트하도록 지정한것 
df = pyupbit.get_ohlcv(ticker="KRW-BTC",interval="month", count=10)
print(df)
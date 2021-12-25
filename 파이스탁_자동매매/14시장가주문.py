import pyupbit  
import pprint

f = open('파이스탁_자동매매/upbit.txt')
lines = f.readlines()
access = lines[0].strip()   # access key '\n'
secret = lines[1].strip()   # secret key '\n'
f.close()

upbit = pyupbit.Upbit(access, secret)   # class instance, object



# 시장가 매수 주문
resp = upbit.buy_market_order("KRW-XRP", 7000)
pprint.pprint(resp)

# 지정가 매도 주문
xrp_balace = upbit.get_balance("KRW-XRP")
resp = upbit.sell_market_order("KRW-XRP", xrp_balace*0.9995)
pprint.pprint(resp)
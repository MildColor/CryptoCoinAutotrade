import pyupbit  
import pprint

f = open('파이스탁_자동매매/upbit.txt')
lines = f.readlines()
access = lines[0].strip()   # access key '\n'
secret = lines[1].strip()   # secret key '\n'
f.close()

upbit = pyupbit.Upbit(access, secret)   # class instance, object

# xrp limit order buy
#xrp_price = pyupbit.get_current_price('KRW-XRP')
#print(xrp_price)

# 지정가 주문을 통해서 매매 금액보다 낮게 주문을 넣기
resp = upbit.buy_limit_order("KRW-XRP", 1000, 5)
pprint.pprint(resp)

# 지정가 매도 주문
xrp_balace = upbit.get_balance("KRW-XRP")
resp = upbit.sell_limit_order("KRW-XRP", 1000, xrp_balace)
pprint.pprint(resp)
import pyupbit  
import pprint

f = open('파이스탁_자동매매/upbit.txt')
lines = f.readlines()
access = lines[0].strip()   # access key '\n'
secret = lines[1].strip()   # secret key '\n'
f.close()

upbit = pyupbit.Upbit(access, secret)   # class instance, object


resp = upbit.buy_limit_order("KRW-XRP", 1000, 7)
pprint.pprint(resp['uuid'])
uuid_xrp = resp['uuid']

upbit.cancel_order(uuid_xrp)





import pyupbit  

f = open('파이스탁_자동매매/upbit.txt')
lines = f.readlines()
access = lines[0].strip()   # access key '\n'
secret = lines[1].strip()   # secret key '\n'
f.close()

upbit = pyupbit.Upbit(access, secret)   # class instance, object
balance_krw = upbit.get_balance("KRW")  # get_balance() 는 하나만 가능
print(balance_krw)
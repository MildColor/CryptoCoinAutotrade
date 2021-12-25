import pyupbit


access = "umt9l0xQxoICPFqEI5bfk6wrTvEaToWMef3WVzq3"          # 본인 값으로 변경
secret = "xl77qNGVKDhGEE7JZlxzMnTXiRUc6ino6T3duXKH"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회

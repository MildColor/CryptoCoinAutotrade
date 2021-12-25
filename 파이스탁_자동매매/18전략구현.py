import pyupbit
import time
import datetime

price = pyupbit.get_current_price("KRW-BTC")
print(price)

# 목표가 구하기
def cal_target(ticker): 
    df = pyupbit.get_ohlcv(ticker, "day")
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high'] - yesterday['low']
    target = today['open'] + yesterday_range * 0.5
    return(target)

# 객체 생성
f = open('파이스탁_자동매매/upbit.txt')
lines = f.readlines()
access = lines[0].strip()   # access key '\n'
secret = lines[1].strip()   # secret key '\n'
f.close()
upbit = pyupbit.Upbit(access, secret)   # class instance, object

# 변수 설정
target = cal_target("KRW-BTC")
op_mode = False # 프로그램을 처음시작한 날은 매수되지 않도록 처리, 현재가가 목표가보다 한 참 위에 있을때 매수를 막기위해
hold = False # 매수를 하지 않은 상황
print(cal_target)

# 1초에 한번 현재시간과 비트고인 현재가 출력
while True: 
    now = datetime.datetime.now()
    # 매도 시도
    if now.hour == 8 and now.minute == 59 and 50 <= now.second <= 59:
        if op_mode is True and hold is True: 
            btc_balance = upbit.get_balance("KRW-BTC")
            upbit.sell_market_order("KRW-BTC", btc_balance)
            hold = False
    
    op_mode = False
    time.sleep(10)


    # 09:00:00 목표가 갱신
    if now.hour == 9 and now.minute == 0 and 20 <= now.second <= 30: 
        target = cal_target("KRW-BTC")
        time.sleep(10) #09:00:20 ~31

    price = pyupbit.get_current_price("KRW-BTC")
 
    # 매초마다 조건을 확인한 후 매수 시도
    if op_mode is True and price is not None and hold is False and price >= target: 
        # 매수
        krw_balance = upbit.get_balance("KRW-BTC")
        upbit.buy_market_order("KRW-BTC", krw_balance)
        hold = True

    # 상태 출력
    print(f"현재시간: {now} 목표가: {target} 현재가: {price} 보유상태: {hold} 동작상태: {op_mode}")
    time.sleep(1)
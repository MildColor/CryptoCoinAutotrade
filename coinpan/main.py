import datetime
import time
import ccxt
import pprint
import pandas as pd
import math
import larry
import futurebestk

# 파일로부터 apiKey, Secret 읽기
with open ("coinpan/api.txt") as f: 
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

# slack 채널, 토큰 
myToken = "xoxb-2918603308486-2918722972518-5SRvKtv98YWjWPJ0nHxVG5uC"
channel = "#information"

# binance 객체 생성, default 값을 future로 
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options':{
        'defaultType':'future' 
    }
}) 

symbol = "BTC/USDT"
ticker = "BTCUSDT"
range = "1d"
# long_k = futurebestk.best_k(symbol,range, long)
# short_k = futurebestk.best_k(symbol,range, short)
# long_target, short_target = larry.cal_target(binance, symbol, long_k, short_k)
long_target, short_target = larry.cal_target(binance, symbol, 0.77, 0.2)
now_pos = larry.now_position(ticker)

# 잔고
balance = binance.fetch_balance(params={"type": "future"})
usdt = balance['total']['USDT']

# Leverage 설정
markets = binance.load_markets()
market = binance.market(symbol)
resp = binance.fapiPrivate_post_leverage({
    'symbol' : market['id'],
    'leverage' : 1
})

position = {
    "type": None,
    "amount": 0
}
op_mode = False # 상태 변수(동작 여부)


# 현재시간, 현재가 출력
while True: 
    # time
    now = datetime.datetime.now()

    # position 종료
    if now.hour == 8 and now.minute == 55 and (0 <= now.second < 10):
        if op_mode and position['type'] is not None:
            larry.exit_position(binance, symbol, position)
            op_mode = False
            larry.post_message(myToken,"#information", f"position close,\n {now_pos}")


    # 9:00:20 ~ 9:00:30 목표가 갱신
    if now.hour == 9 and now.minute == 0 and (20 <= now.second < 30):
        long_target, short_target = larry.cal_target(binance, symbol, long_k=0.77, short_k=0.2)

        # 선물 usdt 잔고 조회
        balance = binance.fetch_balance(params={"type": "future"})
        usdt = balance['total']['USDT']
        op_mode = True

        # 목표가, 잔고 메시지 전송
        larry.post_message(
            myToken, "#informaiton", 
            f"long target:{long_target},\n short target:{short_target},\n Total Balance:{usdt}")
        time.sleep(10)

    # current price, 구매 수량(portion 만큼)
    btc = binance.fetch_ticker(symbol=symbol)
    cur_price = btc['last']
    amount = larry.cal_amount(usdt, cur_price, 1)

    if op_mode and position['type'] is None:
        larry.enter_position(binance, symbol, cur_price, long_target, short_target, amount, position)

        larry.post_message(myToken,"#information", 
            f"position open,\n {now_pos}")

    print(now, cur_price, long_target, short_target)
    time.sleep(1)



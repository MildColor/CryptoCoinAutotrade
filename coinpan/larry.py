import ccxt 
import pandas as pd
import math
import pprint
import requests

# 파일로부터 apiKey, Secret 읽기
with open ("coinpan/api.txt") as f: 
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

# binance 객체 생성, default 값을 future로 
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options':{
        'defaultType':'future' 
    }
})

# 목표가 계산
def cal_target(exchange, symbol, long_k, short_k):
    # symbol에 대한 ohlcv 일봉을 얻기
    data = exchange.fetch_ohlcv(
        symbol=symbol, 
        timeframe= "1d",
        since=None, 
        limit=10
    )
    # 일봉 데이터를 데이터프레임 객체로 변환
    df = pd.DataFrame(
        data=data,
        columns=['datetime', 'open', 'high', 'low', 'close', 'volume']
    )
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)

    # 전일 데이터와 금일 데이터로 목표가 계산
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    long_target = today['open'] + (yesterday['high'] - yesterday['low']) * long_k
    short_target = today['open'] - (yesterday['high'] - yesterday['low']) * short_k
    return long_target, short_target


# 수량 계산
def cal_amount(usdt_balance, cur_price, portion):
    portion = portion
    usdt_trade = usdt_balance * portion
    amount = math.floor((usdt_trade * 1000) / cur_price) / 1000
    return amount


# 포지션 진입, 청산
def enter_position(exchange, symbol, cur_price, long_target, short_target, amount, position):
    if cur_price > long_target:     # long position
        position['type'] = 'long'
        position['amount'] = amount
        exchange.create_market_buy_order(symbol=symbol, amount=amount)
    elif cur_price < short_target:      # short position
        position['type'] = 'short'
        position['amount'] = amount
        exchange.create_market_sel_order(symbol=symbol, amount=amount)

def exit_position(exchange, symbol, position):
    amount = position['amount']
    if position['type'] == 'long':
        exchange.create_market_sel_order(symbol=symbol, amount=amount)
        position['type'] = None
        
    elif position['type'] == 'short':
        exchange.create_market_buy_order(symbol=symbol, amount=amount)    
        position['type'] = None

# 현재 포지션 정보
def now_position(ticker):
    balance = binance.fetch_balance()
    positions = balance['info']['positions'] 

    for position in positions:
        if position['symbol'] == ticker:
            str_pos = str(position)
            str_pos = str_pos.replace("{","")
            str_pos = str_pos.replace("}","")
            str_pos = str_pos.replace(",", "\n")
            
            return(str_pos)
          
           


# Slack
myToken = "xoxb-2918603308486-2918722972518-5SRvKtv98YWjWPJ0nHxVG5uC"
channel = "#information"

# Send a message to channel
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)




import pyupbit
import pprint

orderbooks = pyupbit.get_orderbook("KRW-BTC")
pprint.pprint(orderbooks)

orderbook = orderbooks["orderbook_units"][4]
pprint.pprint(orderbook)

total_ask_size = orderbooks['total_ask_size']
total_bid_size = orderbooks['total_bid_size']

print('매도호가 총합:', total_ask_size)
print('매수호가 총합:', total_bid_size)
import alpaca_trade_api as tradeapi

key='PK85EHCP5TAO0SX29QYM'
secret_key='U1AGrWz74yPEPbiCt01Le6ZZYpYturN27rDcFluy'
endpoint_URL='https://paper-api.alpaca.markets'
api = tradeapi.REST(key, secret_key, endpoint_URL)

api.cancel_all_orders()
def foo():
	return(api.submit_order("BIO", 1, "buy", "limit", "gtc", limit_price=5))

print(foo())
print("---------------------------------")
print(api.list_orders())
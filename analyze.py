import csv
import yfinance as yf
import stockstats as st
import pandas as pd
import alpaca_trade_api as alpaca

def writer(symbol, columns=["Open","High",
						"Low","Close","Volume",
						"Dividends","Stock Splits"]):
	symbol = symbol.upper()
	hist = kdj(yf.Ticker(symbol).history(period="max"))
	hist.to_csv(str(symbol+".csv"), header=columns, sep=",", index=True)

def kdj(symbol):
	kdj_values = pd.read_csv(symbol.upper()+".csv")
	kdj_values["kdjj"] = (st.StockDataFrame.retype(kdj_values).get("kdjj")).to_list()
	return(kdj_values)

def std_dev(_a):
	return _a.std()

def create_orders(symbol, j_values, quantity):
	# read kdj, see if the most recent 
	# J value is less than 20 or above 80
	# if so, return a corresponding order 
	# type (buy or sell) and the name of the stock (ticker symbol)
	print(j_values)
	if j_values.tail(n=1)[0] <= 20:
		print("Creating " + str(quantity) + " sell order(s) for " + str(symbol))
		apca.submit_order(symbol, quantity, "sell", "market", "gtc")
	elif j_values.tail(n=1)[0] >= 80:
		print("Creating " + str(quantity) + " buy order(s) for " + str(symbol))
		apca.submit_order(symbol, quantity, "buy", "market", "gtc")

apca = alpaca.REST(key, secret_key, endpoint_URL)
a = kdj("BIO")
#a["kdj_jd_diff"] = a["kdjj"] - a["kdjd"]
create_orders("BIO", a["kdjj"], 100)

#a columns
'''
Index(['open', 'high', 'low', 'close', 'volume', 'dividends', 'stock splits',
       'rsv_9', 'kdjk_9', 'kdjk', 'kdjd_9', 'kdjd', 'kdjj_9', 'kdjj',
       'kdj_jd_diff'],
      dtype='object')
'''

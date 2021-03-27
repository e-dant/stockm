import csv
import yfinance as yf
import stockstats as st
import pandas as pd
import alpaca_trade_api as alpaca
from sys import path 
from credentials import get_credentials

def writer(symbol, columns=["Open","High",
						"Low","Close","Volume",
						"Dividends","Stock Splits"]):
	symbol = symbol.upper()
	hist = kdj(yf.Ticker(symbol).history(period="max"))
	hist.to_csv(str(symbol+".csv"), header=columns, sep=",", index=True)

def kdj(symbol):
	kdj_values = pd.read_csv("historical/"+symbol.upper()+".csv")
	kdj_values["kdjj"] = (st.StockDataFrame.retype(kdj_values).get("kdjj")).to_list()
	return(kdj_values)

def conditional_order(symbol, j_values, quantity):
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

path.append("historical/")
credentials = get_credentials()
apca = alpaca.REST(credentials["key"], 
			credentials["secret_key"], 
			credentials["endpoint_URL"])
a = kdj("BIO")
#a["kdj_jd_diff"] = a["kdjj"] - a["kdjd"]
conditional_order("BIO", a["kdjj"], 100)
apca.list_orders()

#a columns
'''
Index(['open', 'high', 'low', 'close', 'volume', 'dividends', 'stock splits',
       'rsv_9', 'kdjk_9', 'kdjk', 'kdjd_9', 'kdjd', 'kdjj_9', 'kdjj',
       'kdj_jd_diff'],
      dtype='object')
'''

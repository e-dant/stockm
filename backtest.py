#take a portion of a given csv file and run a hypothetical 
#account through as if the last date on the csv is the current date.
#uses a hypothetical account of $10,000.

import yfinance as yf
import csv
import stockstats as st
import pandas as pd

def writer_BT(symbol, columns=["Open","High",
						"Low","Close","Volume",
						"Dividends","Stock Splits"]):
	hist = yf.Ticker(symbol).history(period="max")
	#hist = yf.Ticker(symbol).history(start="2000-01-01", end="2015-01-01")
	hist.to_csv(str("historical/"+symbol+"_BT.csv"), header=columns, sep=",", index=True)

def kdj(symbol):
	kdj_values = pd.read_csv("historical/"+symbol+"_BT.csv")
	kdj_values = (st.StockDataFrame.retype(kdj_values).get("kdjj")).to_list()
	return(kdj_values)

def conditional_order_BT(symbol, j_values, quantity):
	# read kdj, see if the most recent 
	# J value is less than 20 or above 80
	# if so, log a hypothetical order at 
	# the corresponding market price in the given file
	print(j_values)
	if j_values.tail(n=1)[0] <= 20:
		print("Creating " + str(quantity) + " sell order(s) for " + str(symbol))
		#apca.submit_order(symbol, quantity, "sell", "market", "gtc")
	elif j_values.tail(n=1)[0] >= 80:
		print("Creating " + str(quantity) + " buy order(s) for " + str(symbol))
		#apca.submit_order(symbol, quantity, "buy", "market", "gtc")

symbol = "BIO"
symbol = symbol.upper()
#writer_BT(symbol)
historical = pd.read_csv("historical/"+symbol+"_BT.csv")
#print(historical)
#a=kdj(symbol)
#print(a)
total_equity = 10000
PL = 0
orders = [] #date, side, price
a = kdj(symbol)
b = (yf.Ticker(symbol).history(period="max").index)
c = []
for i in b:
	c.append(i.__str__())
d = zip(a,c)
for i in d:
	print(i)
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
	hist = yf.Ticker(symbol).history(start = '2000-01-01', end = '2020-01-01')
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

def test(arr, size_arr):
	equity = 10000
	PL = 1
	orders = []
	prices = historical['Open'].tolist()
	buys = equity/prices[0]
	equity -= buys * prices[0]
	for i in range(size_arr):
		can_buy = int(equity/prices[i]) > 1
		if arr[i][0] <= 10 and can_buy:
			buys = int((equity/prices[i]))
			print("bought", buys, "shares")
			print('price:'+ str(prices[i]))
			equity -= prices[i] * buys

		elif (arr[i][0] >= 90) and (prices[i] - prices[i-1] > 0):
			print(buys)
			print('sold ' + str(buys) + ' shares')
			print('price:'+ str(prices[i]))
			equity += (prices[i] * buys)
			buys = 0
			print('new equity', equity)
			print()



	print(equity + (buys * prices[i]))

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
b = (yf.Ticker(symbol).history(start = '2000-01-01', end = '2020-01-01').index)
c = []
for i in b:
	c.append(i.__str__())
d = list(zip(a,c))
test(d, len(d))
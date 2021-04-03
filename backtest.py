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

def should_order(j):
	if 80 < j < 20:
		return False
	else:
		return True

def buy_magnitude(j,buyingpower):
	if j >= 100:
		return buyingpower / 10
	elif j >= 90:
		return buyingpower / 20
	elif j >= 80:
		return buyingpower / 40

def sell_magnitude(j,totalshares):
	if j <= 20:
		return totalshares / 40
	elif j <= 10:
		return totalshares / 20
	elif j <= 0:
		return totalshares / 10

def order(side,amount,price,liquidequity,totalshares,date):
	#log the order given
	#update equtiy and current shares
	#returns a list w/ updated order aguments
	if side == 'buy':
		liquidequity -= (amount*price)
		totalshares += amount
	else:
		liquidequity += (amount*price)
		totalshares -= amount

	return [side,amount,price,liquidequity,totalshares,date]

def test(arr, size_arr):
	log = []
	liquidequity = 10000
	prices = historical['Open'].tolist()
	log.append(order('buy', int(liquidequity/prices[0]), prices[0],liquidequity, 0, historical[0]))
	for i in range(size_arr):
		side = ''
		amount = 0
		currentprice = prices[i]
		currentdate = historical[i]
		liquidequity = log[i][3]
		j = arr[i][0]
		can_buy = int(liquidequity/prices[i]) > 1
		if should_order(j):
			#create buy or sell orders based on the magnitude

		if j <= 10 and can_buy:
			buys = int((liquidequity/prices[i]))
			toprint+="buy:  "+ str(buys)+", "
			toprint+='price:'+ str(prices[i])
			equity -= prices[i] * buys

		elif arr[i][0] >= 90:
			amt = int(det_buying_pwr(arr[i][0], liquidequity/prices[i]))
			buys -= amt
			toprint+='sold: ' + str(amt) + ', '
			toprint+='price:'+ str(prices[i])
			#if equity + (prices[i] * buys) < equity:
				#print("we lost boys", prices[i])
			liquidequity += (prices[i] * buys)
			toprint+='new equity'+ str(liquidequity)
		if toprint:
			print(toprint)



	print(liquidequity + (buys * prices[i]), buys)

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
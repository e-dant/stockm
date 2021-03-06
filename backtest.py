#take a portion of a given csv file and run a hypothetical 
#account through as if the last date on the csv is the current date.
#uses a hypothetical account of $10,000.

import yfinance as yf
import csv
import stockstats as st
import pandas as pd

#TODO: Make a Wallet Object

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
	if j >= 100:
		return 'buy'
	elif j <= 0:
		return 'sell'
	else:
		return None

#TODO pass in a new variable to define the range to compare the j value
#TODO such as if (j >= 120) or if (j >= range(n))
def buy_magnitude(j,buyingpower):
	if j >= 120:
		return buyingpower / 10
	elif j >= 110:
		return buyingpower / 20
	elif j >= 100:
		return buyingpower / 40
	else:
		return None

def sell_magnitude(j,total_shares):
	if j <= 0:
		return total_shares / 40
	elif j <= -10:
		return total_shares / 20
	elif j <= -20:
		return total_shares / 10
	else:
		return None

#TODO make a new function to update the variables side, amount, price, liquid_equity, total_shares, date
def order(side, amount, price, liquid_equity, total_shares, date):
	#update equity, log order
	#does not return
	if side == 'buy':
		liquid_equity -= (amount*price)
		total_shares += amount
	else:
		liquid_equity += (amount*price)
		total_shares -= amount
	return([side, amount, price, liquid_equity, total_shares, date])

def update_equity(side, amount, price, last_equity):
	#given the most recent order and current equity return the new equity as a list with 3 elements
	#total liquid equity [0], total number of shares [1], total value of those shares [2]

	#first check to see what side is
	#if side is buy
		#last_equity[0] - (amount * price)
			#last_equity[0] is the total liquid equity (cash)
	#if side is sell last_equity[0] + (amount * price)
	order_liquid = amount * price
	if side == 'buy':
		order_liquid * -1

	new_equity = [last_equity[0] + order_liquid, last_equity[1] + amount,  ]
	return 0

#log object:
# constructor: empty
# methods: convert from data given (from dict, list, tuple, etc)
# print
# append
# list_all
# shape
# convert_from
# convert_to
# getters/setters

class Log:
	def __init__(self):
		#TODO make local variables local variables side, amount, price, liquid_equity, total_shares, date
		#TODO keys by j values??? profit.
		self.a = []
		self.liquid_equity = 0
		self.total_shares = 0

	def pprint(self):
		print(self.a)

	def append(self, b):
		self.update(b)
		self.a.append([b[0], b[1], b[2], self.liquid_equity, self.total_shares, b[5]])

	def __getitem__(self, item):
		return self.a[item]

	def get_last_entry(self):
		return self.a[len(self.a) - 1]

	def update(self, b):
		if b[0] == 'buy':
			self.liquid_equity -= b[3]
			self.total_shares += b[4]
		else:
			self.liquid_equity += b[3]
			self.total_shares -= b[4]

#TODO: Consolidate updating variables into one place ie shares, liquid equity

def bt(j_values, dates, size):
	log = Log()
	liquid_equity = 10000
	prices = pd.read_csv("historical/"+symbol+"_BT.csv")["Open"].tolist()
	#side, amount, price, liquid_equity, total_shares, date
	log.append(['buy', int(liquid_equity/prices[0]), prices[0], liquid_equity, 0, dates[0]])
	#print(log.get_last_entry()[3])
	total_shares = log.get_last_entry()[-2]
	liquid_equity = log.get_last_entry()[3]
	#print(total_shares)
	#print(liquid_equity)
	print(log.get_last_entry())
	for i in range(0,size):
		#print(i)
		#TODO fix indexing isues with log list
		side = ''
		amount = 0
		currentprice = prices[i]
		currentdate = b[i]
		liquid_equity = log.get_last_entry()[3]
		j = j_values[i]
		can_buy = int(liquid_equity/prices[i]) > 1
		#TODO change buy magnitude and sell magnitude to order magnitude
		#TODO pass string from should_order into order_magnitude and determine order magnitude from there
		if should_order(j) == 'buy':
			# TODO update local variables side, amount, price, liquid_equity, total_shares, date
			# TODO DO THE ABOVE OUTSIDE OF THE ORDER FUNCTION
			#create buy or sell orders based on the magnitude
			amount = buy_magnitude(j, liquid_equity)
			log.append(['buy', amount, prices[i], liquid_equity, 0, dates[i]])
		elif should_order(j) == 'sell':
			amount = sell_magnitude(j, liquid_equity)
			log.append(['sell', amount, prices[i], liquid_equity, 0, dates[i]])

	for i in log.a:
		print(i)

		#if j <= 10 and can_buy:
			#buys = int((liquid_equity/prices[i]))
			#toprint+="buy:  "+ str(buys)+", "
			#toprint+='price:'+ str(prices[i])
			#equity -= prices[i] * buys

		#elif j_by_date[i][0] >= 90:
			#amt = int(det_buying_pwr(j_by_date[i][0], liquid_equity/prices[i]))
			#buys -= amt
			#toprint+='sold: ' + str(amt) + ', '
			#toprint+='price:'+ str(prices[i])
			#if equity + (prices[i] * buys) < equity:
				#print("we lost boys", prices[i])
			#liquid_equity += (prices[i] * buys)
			#toprint+='new equity'+ str(liquid_equity)

symbol = "BIO"
symbol = symbol.upper()
#writer_BT(symbol)
#print(historical)
#a=kdj(symbol)
#print(a)
total_equity = 10000
a = kdj(symbol)
b = (yf.Ticker(symbol).history(start = '2000-01-01', end = '2020-01-01').index)
c = []
for i in b:
	c.append(i.__str__())
j_by_date = list(zip(a,c))
#print(j_by_date)
bt(a,c, len(j_by_date))


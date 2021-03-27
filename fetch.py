import csv
import yfinance as yf
#from sys import path 

def writer(symbol, columns=["Open","High",
						"Low","Close","Volume",
						"Dividends","Stock Splits"]):
	symbol = symbol.upper()
	hist = yf.Ticker(symbol).history(period="max")
	hist.to_csv(str("historical/"+symbol.upper()+".csv"), header=columns, sep=",", index=True)

#path.append("historical/")
writer("BIO")


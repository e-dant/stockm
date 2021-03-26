import csv
import yfinance as yf

def writer(symbol, columns=["Open","High",
						"Low","Close","Volume",
						"Dividends","Stock Splits"]):
	symbol = symbol.upper()
	hist = yf.Ticker(symbol).history(period="max")
	hist.to_csv(str(symbol+".csv"), header=columns, sep=",", index=True)

writer("BIO")


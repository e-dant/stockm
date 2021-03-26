import alpaca_trade_api as tradeapi

def getAccountInfo():
	api = tradeapi.REST()
	# Get our account information.
	account = api.get_account()
	# Check if our account is restricted from trading.
	if account.trading_blocked:
		print('Account is currently restricted from trading.')
	# Check how much money we can use to open new positions.
	print('${} is available as buying power.'.format(account.buying_power))

def getGainLoss(key='PK85EHCP5TAO0SX29QYM', 
	secret_key='U1AGrWz74yPEPbiCt01Le6ZZYpYturN27rDcFluy', 
	endpoint_URL='https://paper-api.alpaca.markets'):
	# First, open the API connection
	api = tradeapi.REST(
		key,
		secret_key,
		endpoint_URL
	)

	# Get account info
	account = api.get_account()

	# Check our current balance vs. our balance at the last market close
	balance_change = float(account.equity) - float(account.last_equity)
	print(f'Today\'s portfolio balance change: ${balance_change}')

getAccountInfo()
getGainLoss()
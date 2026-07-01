import yfinance as yf

# Fetch data for Apple stock
ticker = "AAPL"
data = yf.download(ticker, period="5d")

print(data)
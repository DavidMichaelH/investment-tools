import yfinance as yf

msft = yf.Ticker("MSFT")

# get all stock info (slow)
msft.info
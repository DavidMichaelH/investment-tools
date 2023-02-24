import yfinance as yf
import os
import sqlite3


current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
db_file = os.path.join(parent_dir, 'database', 'mydatabase.db')

if not os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
    # create tables, add indexes, etc.
else:
    conn = sqlite3.connect(db_file)


# Define the stock symbol and date range for the data download
symbol = "TSLA"
start_date = "2010-01-01"
end_date = "2022-02-23"

# Creates a Cursor object in Python, which is used to execute SQL statements on the SQLite database
c = conn.cursor()

# Create the table to store the stock data if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS stock_prices
             (symbol text, date text, open real, high real, low real, close real, volume integer)''')

# Download the stock data from Yahoo Finance
data = yf.download(symbol, start=start_date, end=end_date)

# Insert the stock data into the SQLite database
for index, row in data.iterrows():
    c.execute("INSERT INTO stock_prices VALUES (?, ?, ?, ?, ?, ?, ?)",
              (symbol, index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))

# Commit the changes to the database and close the connection
conn.commit()
conn.close()

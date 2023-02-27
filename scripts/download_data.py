import yfinance as yf
import os
import sqlite3


table_name = 'banking_prices'
db_name = 'investment_database.db'
symbols = ["JPM", "BAC", "WFC", "C", "GS", "MS", "USB", "PNC", "COF", "AXP", "DFS", "BBT", "FITB", "KEY", "RF"]

start_date = "2013-01-01"
end_date = "2023-01-01"



current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
db_file = os.path.join(parent_dir, 'database', db_name)
if not os.path.exists(db_file):
    print("database file does not exist")
    conn = sqlite3.connect(db_file)
    # create tables, add indexes, etc.
else:
    conn = sqlite3.connect(db_file)

# Creates a Cursor object in Python, which is used to execute SQL statements on the SQLite database
c = conn.cursor()
# Create the table to store the stock data if it doesn't exist
sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} " \
            f"(symbol text, date text, open real, high real, low real, close real, volume integer)"
c.execute(sql_query)


# Download the stock data from Yahoo Finance for all symbols
data = yf.download(symbols, start=start_date, end=end_date)

# Create a list of tuples to insert into the database
rows = []
for symbol in symbols:
    for index, row in data.iterrows():
        rows.append((symbol, index.strftime('%Y-%m-%d'), row[('Open', symbol)], row[('High', symbol)], row[('Low', symbol)], row[('Close', symbol)], row[('Volume', symbol)]))

# Insert the stock data into the SQLite database in a single transaction
sql_query = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)"
c.executemany(sql_query, rows)

# Commit the changes to the database and close the connection
conn.commit()
conn.close()



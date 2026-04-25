import sqlite3

conn = sqlite3.connect('Porfolio Analytics.db')

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS AUTOINCREMENT(
            id INTEGER PRIMARY KEY,
               ticker TEXT NOT NULL,
               shares REAL NOT NULL,
               buy_price REAL NOT NULL,
               current_price REAL NOT NULL
               )
""")

conn.commit()
conn.close()

def import_holdings(holdings):
    conn = sqlite3.connect("prortfolio.db")
    cursor = conn.cursor()

    for h in holdings:
        
      ticker = h["ticker"]
      shares = h["shares"]
      buy_price = h["buy"]
      current_price = h["current"]

      cursor.execute("""
         INSERT INTO HOLDINGS (ticker, shares, buy_price, current_price)
            VALUES(?, ?, ?, ?)
""" (ticker, shares, buy_price, current_price)), 

conn.commit()
conn.close()

from database import create_holdings_table, insert_holdings, get_all_holdings


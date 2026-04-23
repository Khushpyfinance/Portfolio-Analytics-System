import sqlite3

def create_holdings_table():

    conn = sqlite3.connect('portfolio.db')

    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS holdings(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                shares REAL NOT NULL,
                buy_price REAL NOT NULL,
                current_price REAL NOT NULL
                )
    """)

    conn.commit()
    conn.close()

def insert_holdings(holdings):
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    for h in holdings:
        ticker = h["ticker"]
        shares = h["shares"]
        buy_price = h["buy"]
        current_price = h["current"]

        cursor.execute("""
            INSERT INTO holdings (ticker, shares, buy_price, current_price)
            VALUES (?, ?, ?, ?)
        """, (ticker, shares, buy_price, current_price))

    conn.commit()
    conn.close()

import sqlite3

def get_all_holdings():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ticker, shares, buy_price, current_price
        FROM holdings
    """)

    rows = cursor.fetchall()

    holdings = []

    for row in rows:
        holding = {
            "ticker": row[0],
            "shares": row[1],
            "buy": row[2],
            "current": row[3]
        }
        holdings.append(holding)

    conn.close()

    return holdings
    

def clear_holdings():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM HOLDINGS")

    conn.commit()
    conn.close()


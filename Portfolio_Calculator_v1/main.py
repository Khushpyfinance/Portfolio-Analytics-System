import yfinance as yf
from database import create_holdings_table, insert_holdings, get_all_holdings
import numpy as np
import pandas as pd


def fetch_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")

        if data is None or data.empty:
            print(f"No ticker data was found for {ticker}.")
            return None

        price = data["Close"].iloc[-1]
        return price

    except Exception as e:
        print(f"Could not fetch price for {ticker}: {e}")
        return None


def collect_holding():
    price = None

    while price is None:
        ticker = input("Enter ticker: ").upper()
        price = fetch_price(ticker)

        if price is None:
            print("Try again.")

    shares = float(input("Enter number of shares: "))
    buy_price = float(input("Enter buy price: "))

    holding = {
        "ticker": ticker,
        "shares": shares,
        "buy": buy_price
    }

    return holding

def update_current_prices(holdings):
    for h in holdings:
        ticker = h["ticker"]
        price = fetch_price(ticker)

        if price is not None:
            h["current"] = price
        else:
            print(f"Keeping saved current price for {ticker}.")

    return holdings

def collect_portfolio():
    holdings = []
    num = int(input("How many stocks? "))

    for i in range(num):
        h = collect_holding()
        holdings.append(h)

    return holdings


def calculate_cost(holding):
    return holding["shares"] * holding["buy"]


def calculate_current_value(holding):
    current_price = holding["current"]
    return holding["shares"] * current_price


def calculate_profit(holding):
    return calculate_current_value(holding) - calculate_cost(holding)


def calculate_returns_pct(holding):
    return calculate_profit(holding) / calculate_cost(holding) * 100


def calculate_total_cost(holdings):
    total = 0
    for h in holdings:
        total += calculate_cost(h)
    return total


def calculate_total_current_value(holdings):
    total = 0
    for h in holdings:
        total += calculate_current_value(h)
    return total


def calculate_total_profit(holdings):
    total_current = calculate_total_current_value(holdings)
    total_cost = calculate_total_cost(holdings)
    return total_current - total_cost


def calculate_total_return(holdings):
    return calculate_total_profit(holdings) / calculate_total_cost(holdings) * 100


def calculate_weight(holding, total_portfolio_value):
    if total_portfolio_value == 0:
        return 0
    return calculate_current_value(holding) / total_portfolio_value * 100

def get_best_holding_by_profit(holdings):
    best_holding = None
    best_profit = float("-inf")

    for h in holdings:
        profit = calculate_profit(h)

        if profit > best_profit:
            best_profit = profit
            best_holding = h

    return best_holding

def get_worst_holding_by_profit(holdings):
    worst_holding = None
    worst_profit = float("inf")

    for h in holdings:
        profit = calculate_profit(h)

        if profit < worst_profit:
            worst_profit = profit
            worst_holding = h

    return worst_holding

def get_largest_holding_by_weight(holdings, total_portfolio_value):
    largest_holding = None
    largest_weight = float("-inf")

    for h in holdings:
        weight = calculate_weight(h, total_portfolio_value)

        if weight > largest_weight:
            largest_weight = weight
            largest_holding = h

    return largest_holding

def get_smallest_holding_by_weight(holdings, total_portfolio_value):
    smallest_holding = None
    smallest_weight = float("inf")

    for h in holdings:
        weight = calculate_weight(h, total_portfolio_value)
        if weight < smallest_weight:
            smallest_weight = weight
            smallest_holding = h

    return smallest_holding

def get_top_three(holdings):
    sorted_holdings = sorted(
        holdings,
        key=lambda h: calculate_profit(h),
        reverse=True
    )

    return sorted_holdings[0:3]

def get_bottom_three(holdings):
    sorted_holdings = sorted(
       holdings,
       key=lambda h: calculate_profit(h),
       reverse=False
    )

    return sorted_holdings[0:3]

def get_top_three_by_weight(holdings, total_portfolio_value):
    sorted_holdings = sorted(
        holdings,
        key=lambda h: calculate_weight(h, total_portfolio_value),
        reverse=True
    )

    return sorted_holdings[0:3]

def get_top_three_by_return(holdings):
    sorted_holdings = sorted(
        holdings,
        key=lambda h: calculate_returns_pct(h),
        reverse=True
    )

    return sorted_holdings[0:3]

def count_gainers_losers(holdings):
    gainers = 0
    losers = 0
    flat = 0

    for h in holdings:
        profit = calculate_profit(h)

        if profit > 0:
            gainers += 1
        elif profit < 0:
            losers += 1
        else:
            flat += 1

    return gainers, losers, flat

def calculate_average_return(holdings):
    if len(holdings) == 0:
        return 0

    total_return = 0

    for h in holdings:
        return_percent = calculate_returns_pct(h)
        total_return += return_percent

    average = total_return / len(holdings)

    return average

def check_concentration_risk(holdings, total_value):
    risky_holdings = []

    for h in holdings:
        weight = calculate_weight(h, total_value)

        if weight > 40:
            risky_holdings.append(h)

    return risky_holdings

def get_risky_holdings(holdings, total_value):
    risky_holdings = []

    for h in holdings:
        weight = calculate_weight(h, total_value)

        if weight > 40:
            risky_holdings.append(h)

    return risky_holdings

def calculate_weighted_avg_buy_price(holdings):
    if len(holdings) == 0:
        return 0

    total_cost = 0
    total_shares = 0

    for h in holdings:
        total_cost += calculate_cost(h)
        total_shares += h["shares"]

    if total_shares == 0:
        return 0

    return total_cost / total_shares

import pandas as pd

def export_to_excel(holdings, total_value):
    data = []
    for h in holdings:
        row = {
            "Ticker": h["ticker"],
            "Shares": h["shares"],
            "Buy": h["buy"],
            "Current": h["current"],
            "Cost" : calculate_cost(h),
            "Profit": calculate_profit(h),
            "Return %": calculate_returns_pct(h),
            "Weight": calculate_weight(h, total_value)
        }
        data.append(row)

    df = pd.DataFrame(data)
    
    return df

def export_summary_to_excel(holdings):
    data = []
    g, l, f = count_gainers_losers(holdings)
    data.append({"Metric": "Total Cost", "Value": calculate_total_cost(holdings)})
    data.append({"Metric": "Total Value", "Value": calculate_total_current_value(holdings)})
    data.append({"Metric": "Total Profit", "Value": calculate_total_profit(holdings)})
    data.append({"Metric": "Total Return", "Value": calculate_total_return(holdings)})
    data.append({"Metric": "Average Return", "Value": calculate_average_return(holdings)})
    data.append({"Metric": "Weighted Average Buy Price", "Value": calculate_weighted_avg_buy_price(holdings)})
    data.append({"Metric": "Gainers", "Value": g})
    data.append({"Metric": "Losers", "Value": l}) 
    data.append({"Metric": "Flat", "Value": f})  
    

    df = pd.DataFrame(data)

    return df

def export_insights_to_excel(holdings, total_value):
    data = []

    best = get_best_holding_by_profit(holdings)
    data.append({
        "Category": "Best by Profit",
        "Rank": 1,
        "Ticker": best["ticker"],
        "Value": calculate_profit(best)
    })

    worst = get_worst_holding_by_profit(holdings)
    data.append({
        "Category": "Worst by Profit",
        "Rank": 1,
        "Ticker": worst["ticker"],
        "Value": calculate_profit(worst)
    })

    largest = get_largest_holding_by_weight(holdings, total_value)
    data.append({
        "Category": "Largest by Weight",
        "Rank": 1,
        "Ticker": largest["ticker"],
        "Value": calculate_weight(largest, total_value)
    })

    smallest = get_smallest_holding_by_weight(holdings, total_value)
    data.append({
        "Category": "Smallest by Weight",
        "Rank": 1,
        "Ticker": smallest["ticker"],
        "Value": calculate_weight(smallest, total_value)
    })

    risky = get_risky_holdings(holdings, total_value)

    if len(risky) == 0:
        data.append({
            "Category": "Concentration Warning",
            "Rank": 1,
            "Ticker": "None",
            "Value": "No concentration risk detected"
        })
    else:
        rank = 1
        for h in risky:
            data.append({
                "Category": "Concentration Warning",
                "Rank": rank,
                "Ticker": h["ticker"],
                "Value": calculate_weight(h, total_value)
            })
            rank += 1
    df = pd.DataFrame(data)
    
    return df

def export_rankings_to_excel(holdings, total_value):
    data = []

    top_three = get_top_three(holdings)
    rank = 1
    for h in top_three:
        data.append({
            "Category": "Top 3 by Profit",
            "Rank": rank,
            "Ticker": h["ticker"],
            "Value": calculate_profit(h)
        })
        rank += 1

    bottom_three = get_bottom_three(holdings)
    rank = 1
    for h in bottom_three:
        data.append({
            "Category": "Bottom 3 by Profit",
            "Rank": rank,
            "Ticker": h["ticker"],
            "Value": calculate_profit(h)
        })
        rank += 1

    top_weight = get_top_three_by_weight(holdings, total_value)
    rank = 1
    for h in top_weight:
        data.append({
            "Category": "Top 3 by Weight",
            "Rank": rank,
            "Ticker": h["ticker"],
            "Value": calculate_weight(h, total_value)
        })
        rank += 1

    top_return = get_top_three_by_return(holdings)
    rank = 1
    for h in top_return:
        data.append({
            "Category": "Top 3 by Return %",
            "Rank": rank,
            "Ticker": h["ticker"],
            "Value": calculate_returns_pct(h)
        })
        rank += 1

    df = pd.DataFrame(data)

    return df

def fetch_historical_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period ="1y")
    return data

data= fetch_historical_data("APPL")
data["Daily Return"] = data["close"].pct_change()

print(data[["Close", "Daily Return"]].head())

daily_volatility = data["Daily Return"].std()
annual_volatility = daily_volatility * (252 ** 0.5)

print("Daily Volatility:", daily_volatility)
print("Annual Volatility:", annual_volatility)

def calculate_portfolio_1y_return(holdings):
    total_value = calculate_total_current_value(holdings)

    portfolio_return = 0

    for h in holdings:
        ticker = h["ticker"]

        # weight (convert to decimal)
        weight = calculate_weight(h, total_value) / 100

        # fetch 1-year data
        data = fetch_historical_data(ticker)

        # skip if no data
        if data.empty:
            continue

        start_price = data["Close"].iloc[0]
        end_price = data["Close"].iloc[-1]

        stock_return = (end_price - start_price) / start_price

        portfolio_return += weight * stock_return

    return portfolio_return * 100

def calculate_benchmark_1y_return():
    data = fetch_historical_data("^GSPC")

    if data.empty:
        return 0

    start_price = data["Close"].iloc[0]
    end_price = data["Close"].iloc[-1]

    benchmark_return = (end_price - start_price) / start_price

    return benchmark_return * 100

def compare_portfolio_to_benchmark(holdings):
    portfolio_return = calculate_portfolio_1y_return(holdings)
    benchmark_return = calculate_benchmark_1y_return()

    difference = portfolio_return - benchmark_return

    return portfolio_return, benchmark_return, difference


def main():
    print("Portfolio Analytics System (V3)")

    print("Portfolio Summary")

    create_holdings_table()

    choice = input("Enter 1 for new portfolio or 2 to load saved portfolio: ")

    print("Portfolio Analytics System (V3)")
    print("Portfolio Summary")

    create_holdings_table()

    choice = input("Enter 1 for new portfolio or 2 to load saved portfolio: ")

    if choice == "1":
        save_choice = input("Enter R to replace old portfolio or A to add to existing portfolio: ").upper()
        from database import clear_holdings
        
        if save_choice == "R":
            clear_holdings()
            holdings = collect_portfolio()
            update_current_prices(holdings)
            insert_holdings(holdings)

        elif save_choice == "A":
            new_holdings = collect_portfolio()
            update_current_prices(new_holdings)
            insert_holdings(new_holdings)
            holdings = get_all_holdings()
            update_current_prices(holdings)

        else:
            print("Invalid choice.")
            return

    elif choice == "2":
        holdings = get_all_holdings()
        update_current_prices(holdings)

    else:
        print("Invalid choice.")
        return
                      
    
    print(f"Total Cost: {round(calculate_total_cost(holdings), 2)}")
    print(f"Total Current Value: {round(calculate_total_current_value(holdings), 2)}")
    print(f"Total Profit/Loss: {round(calculate_total_profit(holdings), 2)}")
    print(f"The total return is: {round(calculate_total_return(holdings), 2)}%")

    print("\n-----------------")
    print("Holdings Breakdown")
    print("-----------------")

    total_value = calculate_total_current_value(holdings)

    for h in holdings:
        ticker = h["ticker"]
        shares = h["shares"]
        buy_price = h["buy"]

        cost = calculate_cost(h)
        current_value = calculate_current_value(h)
        profit_value = calculate_profit(h)
        return_pct = calculate_returns_pct(h)
        weight = calculate_weight(h, total_value)

        print(f"Ticker: {ticker}")
        print(f"  Shares: {shares}")
        print(f"  Buy Price: {buy_price}")
        print(f"  Cost: {round(cost, 2)}")
        print(f"  Current Value: {round(current_value, 2)}")
        print(f"  Profit/Loss: {round(profit_value, 2)}")
        print(f"  Return: {round(return_pct, 2)}%")
        print(f"  Weight: {round(weight, 2)}%")
        print()

    print("\n-----------------")
    print("Portfolio Insights")
    print("-----------------")

    best_holding = get_best_holding_by_profit(holdings)
    ticker = best_holding["ticker"]
    profit = calculate_profit(best_holding)
    print(f"Best Holding: {ticker}")
    print(f"Profit: {round(profit, 2)}")

    worst_holding = get_worst_holding_by_profit(holdings)
    ticker = worst_holding["ticker"]
    profit = calculate_profit(worst_holding)
    print(f"Worst Holding: {ticker}")
    print(f"Profit: {round(profit, 2)}")

    largest_holding = get_largest_holding_by_weight(holdings, total_value)
    ticker = largest_holding["ticker"]
    weight = calculate_weight(largest_holding, total_value)
    print(f"Largest Holding: {ticker}")
    print(f"Weight Percentage: {round(weight, 2)}%")

    smallest_holding = get_smallest_holding_by_weight(holdings, total_value)
    ticker = smallest_holding["ticker"]
    weight = calculate_weight(smallest_holding, total_value)
    print(f"Smallest Holding: {ticker}")
    print(f"Weight Percentage: {round(weight, 2)}%")

    top_three = get_top_three(holdings)

    print("\nTop 3 Holdings by Profit")
    print("-----------------------")

    rank = 1
    for h in top_three:
        ticker = h["ticker"]
        profit = calculate_profit(h)
        print(f"{rank}. {ticker} → {round(profit, 2)}")
        rank += 1

    bottom_three = get_bottom_three(holdings)

    print("\nBottom 3 Holdings by Profit")
    print("-----------------------")

    rank = 1
    for h in bottom_three:
        ticker = h["ticker"]
        profit = calculate_profit(h)
        print(f"{rank}. {ticker} → {round(profit, 2)}")
        rank += 1

    top_three_weight = get_top_three_by_weight(holdings, total_value)

    print("\nTop 3 Holdings by Weight")
    print("-----------------------")

    rank = 1
    for h in top_three_weight:
        ticker = h["ticker"]
        weight = calculate_weight(h, total_value)
        print(f"{rank}. {ticker} → {round(weight, 2)}%")
        rank += 1

    top_three_return = get_top_three_by_return(holdings)

    print("\nTop 3 Holdings by Return %")
    print("-----------------------")

    rank = 1
    for h in top_three_return:
        ticker = h["ticker"]
        return_pct = calculate_returns_pct(h)
        print(f"{rank}. {ticker} → {round(return_pct, 2)}%")
        rank += 1

    g, l, f = count_gainers_losers(holdings)

    print("\nNumber of Gainers and Losers")
    print("-----------------------")
    print(f"Gainers: {g}")
    print(f"Losers: {l}")
    print(f"Flat: {f}")

    avg_return = calculate_average_return(holdings)

    print("\nAverage Return Across Holdings")
    print("-----------------------------")
    print(f"Average Return: {round(avg_return, 2)}%")

    risky = get_risky_holdings(holdings, total_value)

    print("\n⚠ Concentration Warning")
    print("-----------------------")

    if len(risky) == 0:
        print("No concentration risk detected.")
    else:
        for h in risky:
            ticker = h["ticker"]
            weight = calculate_weight(h, total_value)
            print(f"{ticker} → {round(weight, 2)}% (Too high)")

    avg_buy = calculate_weighted_avg_buy_price(holdings)

    print("\nWeighted Average Buy Price")
    print("--------------------------")
    print(f"Average Buy Price: {round(avg_buy, 2)}")

    print("\nPortfolio Weights")
    for h in holdings:
        weight = calculate_weight(h, total_value)
        print(f"{h['ticker']} weight: {round(weight, 2)}%")

    holdings_df = export_to_excel(holdings, total_value)
    print("\nExcel file exported successfully.")

    summary_df = export_summary_to_excel(holdings)
    print("\nExcel file exported successfully.")

    insights_df = export_insights_to_excel(holdings, total_value)
    print("\nExcel file exported successfully.")

    rankings_df = export_rankings_to_excel(holdings, total_value)
    print("\nExcel file exported successfully.")

    portfolio_1y, benchmark_1y, diff = compare_portfolio_to_benchmark(holdings)

    print("\n1-Year Benchmark Comparison")
    print("---------------------------")
    print(f"Portfolio 1Y Return: {round(portfolio_1y, 2)}%")
    print(f"S&P 500 1Y Return: {round(benchmark_1y, 2)}%")
    print(f"Outperformance: {round(diff, 2)}%")

    with pd.ExcelWriter("Portfolio_Analytics_System.xlsx") as writer:
        holdings_df.to_excel(writer, sheet_name="Holdings", index=False)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        insights_df.to_excel(writer, sheet_name="Insights", index=False)
        rankings_df.to_excel(writer, sheet_name="Rankings", index=False)


if __name__ == "__main__":
    main()

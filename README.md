Portfolio Analytics System (Python)

A Python-based portfolio analytics system that calculates returns, risk metrics, and performance relative to the market.

---

## Features

### Core Portfolio Metrics
- Total cost, value, and profit/loss
- Return percentage per holding
- Portfolio-level return
- Position weights

### Portfolio Insights
- Best and worst performing holdings
- Top and bottom performers
- Gainers vs losers breakdown
- Concentration risk detection

### Layer 6 — Advanced Analytics
- Portfolio vs S&P 500 benchmark comparison
- 1-year portfolio return vs benchmark
- Annualized portfolio volatility
- Sharpe ratio (risk-adjusted performance)
- Maximum drawdown analysis
- Historical portfolio value tracking

---

## Technologies Used

- Python
- yfinance (market data)
- pandas & numpy (data processing)
- SQLite (portfolio storage)
- Excel export (reporting)

---

## How It Works

1. User inputs portfolio holdings
2. System fetches real-time market data
3. Calculates portfolio metrics and risk measures
4. Compares performance against the S&P 500
5. Exports results to Excel

---

## Example Output

The system generates an Excel file with:

- Holdings breakdown
- Summary metrics
- Insights and rankings
- Historical portfolio value

---

## Future Improvements

- Rebalancing suggestions
- Scenario / what-if analysis
- Dividend income tracking
- Multi-currency support

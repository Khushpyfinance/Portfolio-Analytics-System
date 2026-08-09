# Portfolio Analytics System

## Overview

Portfolio Analytics System is a Python-based investment analytics platform designed to evaluate portfolio performance, risk, concentration, and benchmark-relative results.

The system combines live market data with locally stored portfolio holdings to calculate security-level and portfolio-level metrics, evaluate risk-adjusted performance, compare results against the S&P 500, track historical portfolio value, and export structured analytics for further reporting in Excel and Power BI.

This project represents an earlier stage in the development of my investment research and portfolio management systems, with a focus on building an end-to-end analytics workflow using Python, SQLite, Excel, and Power BI.

---

## System Architecture

The application follows a simple analytical workflow:

```text
Portfolio Holdings
        ↓
SQLite Storage
        ↓
Market Data Retrieval
        ↓
Portfolio Valuation
        ↓
Performance & Risk Analytics
        ↓
Benchmark Comparison
        ↓
Excel Reporting
        ↓
Power BI Visualization
```

---

## Core Portfolio Analytics

The system calculates portfolio and security-level metrics including:

- Total portfolio cost
- Current portfolio value
- Total profit and loss
- Portfolio return
- Individual holding returns
- Position weights
- Weighted average purchase price
- Gainers, losers, and flat positions

---

## Portfolio Insights

The analytics layer identifies important characteristics of the portfolio, including:

- Best and worst holdings by profit
- Top and bottom holdings by performance
- Largest and smallest positions
- Top holdings by portfolio weight
- Top holdings by percentage return
- Portfolio concentration warnings

These outputs provide a structured view of both performance and portfolio composition.

---

## Risk-Adjusted Performance

The system extends basic portfolio reporting with additional risk analytics.

### Portfolio Volatility

Historical daily returns are used to estimate annualized portfolio volatility.

### Sharpe Ratio

Portfolio performance is evaluated relative to a configurable risk-free rate to estimate risk-adjusted return.

### Maximum Drawdown

Historical portfolio value is reconstructed using market data to measure the largest peak-to-trough decline over the analysis period.

### Historical Portfolio Value

The system reconstructs the historical value of the portfolio based on historical security prices and position sizes.

---

## Benchmark Analysis

Portfolio performance is compared against the S&P 500.

The system calculates:

- 1-year portfolio return
- 1-year S&P 500 return
- Portfolio outperformance or underperformance

This provides a simple benchmark-relative view of portfolio performance rather than evaluating returns in isolation.

---

## Data Persistence

Portfolio holdings are stored locally using SQLite.

The database layer supports:

- Creating the holdings table
- Saving portfolio positions
- Loading previously stored portfolios
- Adding new positions
- Replacing an existing portfolio
- Clearing stored holdings

The database path is resolved relative to the application, allowing the system to operate consistently regardless of the directory from which it is launched.

---

## Excel Reporting

The application generates a structured Excel workbook containing multiple analytical views.

Generated worksheets include:

- **Holdings** — security-level portfolio information
- **Summary** — portfolio performance and risk metrics
- **Insights** — key portfolio observations and concentration warnings
- **Rankings** — top and bottom holdings across several measures
- **Historical Value** — reconstructed historical portfolio value

This creates a reporting layer that can also be used for additional analysis and visualization.

---

## Power BI Dashboard

Portfolio analytics were also visualized through a Power BI dashboard, extending the Python and Excel workflow into an interactive business intelligence layer.

![Power BI Dashboard](Power%20BI%20Screenshot.png)

The repository also includes the Power BI project file for further exploration of the reporting layer.

---

## Technology Stack

- **Python** — analytics and application logic
- **pandas** — data manipulation and reporting
- **yfinance** — current and historical market data
- **SQLite** — portfolio persistence
- **Excel** — structured analytical output
- **Power BI** — portfolio visualization and reporting

---

## Project Structure

```text
Portfolio-Analytics-System/
│
├── main.py
├── database.py
├── requirements.txt
├── Portfolio Dashboard.pbix
├── Power BI Screenshot.png
├── README.md
└── .gitignore
```

### `main.py`

Contains the primary portfolio analytics workflow, including market-data retrieval, portfolio calculations, risk analytics, benchmark comparison, ranking logic, and Excel reporting.

### `database.py`

Provides the SQLite persistence layer used to save, retrieve, and manage portfolio holdings.

---

## Running the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd Portfolio-Analytics-System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python main.py
```

The application allows the user to either create a new portfolio or load an existing portfolio from SQLite.

---

## Current Status

Portfolio Analytics System is complete as an early portfolio analytics and reporting project.

The current version includes portfolio valuation, performance analysis, benchmark comparison, volatility analysis, Sharpe ratio calculation, maximum drawdown analysis, historical portfolio reconstruction, SQLite persistence, Excel reporting, and Power BI visualization.

The project also serves as an earlier step in the development of more advanced investment research and portfolio management systems.

---

## Future Development

Potential extensions include:

- Portfolio rebalancing recommendations
- Scenario and what-if analysis
- Dividend income analytics
- Multi-currency portfolio support
- Expanded benchmark analysis
- Additional portfolio risk measures

---

## Disclaimer

This project is intended for educational and research purposes only.

Nothing in this repository constitutes investment advice or a recommendation to buy or sell securities.
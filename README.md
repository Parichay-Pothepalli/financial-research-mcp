# Financial Datasets MCP Server

A financial data provider MCP server built with [Smithery CLI](https://smithery.ai/docs/getting_started/quickstart_build_python)

## Features

This MCP server provides tools for accessing financial data including:

- Income statements
- Balance sheets
- Cash flow statements
- Current stock prices
- Historical stock prices
- Company news
- SEC filings
- Cryptocurrency prices and information

## Prerequisites

- **Smithery API key**: Get yours at [smithery.ai/account/api-keys](https://smithery.ai/account/api-keys)
- **Financial Datasets API key** (optional): Can be provided through:
  - Environment variable: `FINANCIAL_DATASETS_API_KEY`
  - Session configuration when connecting to the server

## Configuration

The server accepts the following configuration parameters:

- `api_key`: Your Financial Datasets API key (optional)
- `pirate_mode`: Speak like a pirate (for fun, default: false)

## Getting Started

1. Set up your environment:
   ```bash
   # Optional: Create a .env file with your API key
   echo "FINANCIAL_DATASETS_API_KEY=your_api_key_here" > .env
   ```

2. Run the server:
   ```bash
   uv run dev
   ```

3. Test interactively:
   ```bash
   uv run playground
   ```

## Available Tools

- `get_income_statements`: Get income statements for a company
- `get_balance_sheets`: Get balance sheets for a company
- `get_cash_flow_statements`: Get cash flow statements for a company
- `get_current_stock_price`: Get the current/latest price of a company
- `get_historical_stock_prices`: Get historical stock prices for a company
- `get_company_news`: Get news for a company
- `get_available_crypto_tickers`: Get all available crypto tickers
- `get_historical_crypto_prices`: Get historical prices for a cryptocurrency
- `get_current_crypto_price`: Get the current/latest price of a cryptocurrency
- `get_sec_filings`: Get SEC filings for a company

## Development

Your server code is in `src/hello_server/server.py`. Add or update your server capabilities there.

## Deploy

Ready to deploy? Push your code to GitHub and deploy to Smithery:

1. Create a new repository at [github.com/new](https://github.com/new)

2. Initialize git and push to GitHub:
   ```bash
   git add .
   git commit -m "Financial Datasets MCP Server"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. Deploy your server to Smithery at [smithery.ai/new](https://smithery.ai/new)
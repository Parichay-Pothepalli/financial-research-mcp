"""
Financial Datasets MCP Server for Smithery

This server provides financial data tools for accessing stock prices, financial statements,
crypto prices, and SEC filings through the Model Context Protocol.
"""

import json
import os
import httpx
import logging
import sys
import datetime
from typing import Dict, List, Optional, Union, Any
from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from smithery.decorators import smithery

# Configure logging to write to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("financial-datasets-mcp")

# Constants
FINANCIAL_DATASETS_API_BASE = "https://api.financialdatasets.ai"


# Optional: If you want to receive session-level config from user, define it here
class ConfigSchema(BaseModel):
    api_key: str = Field("", description="Your Financial Datasets API key (optional)")
    pirate_mode: bool = Field(False, description="Speak like a pirate (for fun)")


# Helper function to make API requests
async def make_request(url: str, ctx: Context) -> dict[str, any] | None:
    """Make a request to the Financial Datasets API with proper error handling."""
    # Load environment variables from .env file
    load_dotenv()
    
    headers = {}
    # First try to get API key from session config
    session_config = ctx.session_config
    if session_config and session_config.api_key:
        headers["X-API-KEY"] = session_config.api_key
    # Fall back to environment variable if not in session config
    elif api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"Error": str(e)}


@smithery.server(config_schema=ConfigSchema)
def create_server():
    """Create and configure the MCP server."""

    # Create your FastMCP server
    server = FastMCP("Financial Datasets")

    @server.tool()
    async def get_income_statements(
        ticker: str,
        period: str = "annual",
        limit: int = 4,
        ctx: Context = None,
    ) -> str:
        """Get income statements for a company.

        Args:
            ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
            period: Period of the income statement (e.g. annual, quarterly, ttm)
            limit: Number of income statements to return (default: 4)
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/financials/income-statements/?ticker={ticker}&period={period}&limit={limit}"
        data = await make_request(url, ctx)

        # Check if data is found
        if not data:
            return "Unable to fetch income statements or no income statements found."

        # Extract the income statements
        income_statements = data.get("income_statements", [])

        # Check if income statements are found
        if not income_statements:
            return "Unable to fetch income statements or no income statements found."

        # Stringify the income statements
        return json.dumps(income_statements, indent=2)

    @server.tool()
    async def get_balance_sheets(
        ticker: str,
        period: str = "annual",
        limit: int = 4,
        ctx: Context = None,
    ) -> str:
        """Get balance sheets for a company.

        Args:
            ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
            period: Period of the balance sheet (e.g. annual, quarterly, ttm)
            limit: Number of balance sheets to return (default: 4)
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/financials/balance-sheets/?ticker={ticker}&period={period}&limit={limit}"
        data = await make_request(url, ctx)

        # Check if data is found
        if not data:
            return "Unable to fetch balance sheets or no balance sheets found."

        # Extract the balance sheets
        balance_sheets = data.get("balance_sheets", [])

        # Check if balance sheets are found
        if not balance_sheets:
            return "Unable to fetch balance sheets or no balance sheets found."

        # Stringify the balance sheets
        return json.dumps(balance_sheets, indent=2)

    @server.tool()
    async def get_cash_flow_statements(
        ticker: str,
        period: str = "annual",
        limit: int = 4,
        ctx: Context = None,
    ) -> str:
        """Get cash flow statements for a company.

        Args:
            ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
            period: Period of the cash flow statement (e.g. annual, quarterly, ttm)
            limit: Number of cash flow statements to return (default: 4)
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/financials/cash-flow-statements/?ticker={ticker}&period={period}&limit={limit}"
        data = await make_request(url, ctx)

        # Check if data is found
        if not data:
            return "Unable to fetch cash flow statements or no cash flow statements found."

        # Extract the cash flow statements
        cash_flow_statements = data.get("cash_flow_statements", [])

        # Check if cash flow statements are found
        if not cash_flow_statements:
            return "Unable to fetch cash flow statements or no cash flow statements found."

        # Stringify the cash flow statements
        return json.dumps(cash_flow_statements, indent=2)

    @server.tool()
    async def get_current_stock_price(ticker: str, ctx: Context = None) -> str:
        """Get the current / latest price of a company.

        Args:
            ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/prices/snapshot/?ticker={ticker}"
        data = await make_request(url, ctx)

        # Check if data is found
        if not data:
            return "Unable to fetch current price or no current price found."

        # Extract the current price
        snapshot = data.get("snapshot", {})

        # Check if current price is found
        if not snapshot:
            return "Unable to fetch current price or no current price found."

        # Stringify the current price
        return json.dumps(snapshot, indent=2)

    @server.tool()
    async def get_historical_stock_prices(
        ticker: str,
        start_date: str,
        end_date: str,
        interval: str = "day",
        interval_multiplier: int = 1,
        ctx: Context = None,
    ) -> str:
        """Gets historical stock prices for a company.

        Args:
            ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
            start_date: Start date of the price data (e.g. 2020-01-01)
            end_date: End date of the price data (e.g. 2020-12-31)
            interval: Interval of the price data (e.g. minute, hour, day, week, month)
            interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
        data = await make_request(url, ctx)

        # Check if data is found
        if not data:
            return "Unable to fetch prices or no prices found."

        # Extract the prices
        prices = data.get("prices", [])

        # Check if prices are found
        if not prices:
            return "Unable to fetch prices or no prices found."

        # Stringify the prices
        return json.dumps(prices, indent=2)

    @server.tool()
    async def get_company_news(ticker: str, ctx: Context = None) -> str:
        """Get news for a company.

        Args:
            ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/news/?ticker={ticker}"
        data = await make_request(url, ctx)

        # Check if data is found
        if not data:
            return "Unable to fetch news or no news found."

        # Extract the news
        news = data.get("news", [])

        # Check if news are found
        if not news:
            return "Unable to fetch news or no news found."
        return json.dumps(news, indent=2)

    @server.tool()
    async def get_available_crypto_tickers(ctx: Context = None) -> str:
        """
        Gets all available crypto tickers.
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/tickers"
        data = await make_request(url, ctx)

        # Check if data is found
        if not data:
            return "Unable to fetch available crypto tickers or no available crypto tickers found."

        # Extract the available crypto tickers
        tickers = data.get("tickers", [])

        # Stringify the available crypto tickers
        return json.dumps(tickers, indent=2)

    @server.tool()
    async def get_historical_crypto_prices(
        ticker: str,
        start_date: str,
        end_date: str,
        interval: str = "day",
        interval_multiplier: int = 1,
        ctx: Context = None,
    ) -> str:
        """Gets historical prices for a crypto currency.

        Args:
            ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
            start_date: Start date of the price data (e.g. 2020-01-01)
            end_date: End date of the price data (e.g. 2020-12-31)
            interval: Interval of the price data (e.g. minute, hour, day, week, month)
            interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
        data = await make_request(url, ctx)

        # Check if data is found
        if not data:
            return "Unable to fetch prices or no prices found."

        # Extract the prices
        prices = data.get("prices", [])

        # Check if prices are found
        if not prices:
            return "Unable to fetch prices or no prices found."

        # Stringify the prices
        return json.dumps(prices, indent=2)

    @server.tool()
    async def get_current_crypto_price(ticker: str, ctx: Context = None) -> str:
        """Get the current / latest price of a crypto currency.

        Args:
            ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/snapshot/?ticker={ticker}"
        data = await make_request(url, ctx)

        # Check if data is found
        if not data:
            return "Unable to fetch current price or no current price found."

        # Extract the current price
        snapshot = data.get("snapshot", {})

        # Check if current price is found
        if not snapshot:
            return "Unable to fetch current price or no current price found."

        # Stringify the current price
        return json.dumps(snapshot, indent=2)

    @server.tool()
    async def get_sec_filings(
        ticker: str,
        limit: int = 10,
        filing_type: str | None = None,
        ctx: Context = None,
    ) -> str:
        """Get all SEC filings for a company.

        Args:
            ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
            limit: Number of SEC filings to return (default: 10)
            filing_type: Type of SEC filing (e.g. 10-K, 10-Q, 8-K)
        """
        # Fetch data from the API
        url = f"{FINANCIAL_DATASETS_API_BASE}/filings/?ticker={ticker}&limit={limit}"
        if filing_type:
            url += f"&filing_type={filing_type}"
 
        # Call the API
        data = await make_request(url, ctx)

        # Extract the SEC filings
        filings = data.get("filings", [])

        # Check if SEC filings are found
        if not filings:
            return f"Unable to fetch SEC filings or no SEC filings found."

        # Stringify the SEC filings
        return json.dumps(filings, indent=2)

    @server.tool()
    async def analyze_financial_ratios(
        ticker: str,
        time_period: str = "latest",  # Options: "latest", "quarterly", "annual", "5y"
        ratio_types: str = "all",  # Options: "all", "profitability", "valuation", "liquidity", "solvency"
        ctx: Context = None,
    ) -> str:
        """Analyze financial ratios for a company.
        
        Args:
            ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
            time_period: Time period for analysis (latest, quarterly, annual, 5y)
            ratio_types: Types of ratios to include (all, profitability, valuation, liquidity, solvency)
        """
        try:
            # Determine the period and limit based on time_period
            if time_period == "latest":
                period = "quarterly"
                limit = 1
            elif time_period == "quarterly":
                period = "quarterly"
                limit = 4  # Last 4 quarters
            elif time_period == "annual":
                period = "annual"
                limit = 1
            elif time_period == "5y":
                period = "annual"
                limit = 5  # Last 5 years
            else:
                period = "quarterly"
                limit = 1
            
            # Fetch required financial data
            # 1. Income Statements
            income_url = f"{FINANCIAL_DATASETS_API_BASE}/financials/income-statements/?ticker={ticker}&period={period}&limit={limit}"
            income_data = await make_request(income_url, ctx)
            if not income_data or "income_statements" not in income_data or not income_data["income_statements"]:
                return json.dumps({"error": "Unable to fetch income statements for ratio analysis."}, indent=2)
            
            income_statements = income_data["income_statements"]
            
            # 2. Balance Sheets
            balance_url = f"{FINANCIAL_DATASETS_API_BASE}/financials/balance-sheets/?ticker={ticker}&period={period}&limit={limit}"
            balance_data = await make_request(balance_url, ctx)
            if not balance_data or "balance_sheets" not in balance_data or not balance_data["balance_sheets"]:
                return json.dumps({"error": "Unable to fetch balance sheets for ratio analysis."}, indent=2)
            
            balance_sheets = balance_data["balance_sheets"]
            
            # 3. Cash Flow Statements
            cash_flow_url = f"{FINANCIAL_DATASETS_API_BASE}/financials/cash-flow-statements/?ticker={ticker}&period={period}&limit={limit}"
            cash_flow_data = await make_request(cash_flow_url, ctx)
            if not cash_flow_data or "cash_flow_statements" not in cash_flow_data or not cash_flow_data["cash_flow_statements"]:
                return json.dumps({"error": "Unable to fetch cash flow statements for ratio analysis."}, indent=2)
            
            cash_flow_statements = cash_flow_data["cash_flow_statements"]
            
            # 4. Current Stock Price (for valuation ratios)
            price_url = f"{FINANCIAL_DATASETS_API_BASE}/prices/snapshot/?ticker={ticker}"
            price_data = await make_request(price_url, ctx)
            if not price_data or "snapshot" not in price_data or not price_data["snapshot"]:
                return json.dumps({"error": "Unable to fetch current stock price for ratio analysis."}, indent=2)
            
            stock_price = price_data["snapshot"].get("price", 0)
            market_cap = price_data["snapshot"].get("market_cap", 0)
            
            # Calculate financial ratios based on the data
            ratios = {}
            analysis = {}
            
            # Process each time period
            for i in range(min(len(income_statements), len(balance_sheets), len(cash_flow_statements))):
                income = income_statements[i]
                balance = balance_sheets[i]
                cash_flow = cash_flow_statements[i]
                
                period_date = income.get("date", "Unknown")
                period_ratios = {}
                period_analysis = {}
                
                # Extract key financial metrics
                revenue = income.get("revenue", 0)
                net_income = income.get("net_income", 0)
                operating_income = income.get("operating_income", 0)
                
                total_assets = balance.get("total_assets", 0)
                current_assets = balance.get("current_assets", 0)
                total_liabilities = balance.get("total_liabilities", 0)
                current_liabilities = balance.get("current_liabilities", 0)
                total_equity = balance.get("total_equity", 0)
                total_debt = balance.get("long_term_debt", 0) + balance.get("short_term_debt", 0)
                
                operating_cash_flow = cash_flow.get("operating_cash_flow", 0)
                
                # Calculate shares outstanding and EPS
                shares_outstanding = market_cap / stock_price if stock_price > 0 else 0
                eps = net_income / shares_outstanding if shares_outstanding > 0 else 0
                
                # Calculate ratios based on ratio_types parameter
                if ratio_types in ["all", "profitability"]:
                    # Profitability Ratios
                    if total_equity > 0:
                        roe = (net_income / total_equity) * 100
                        period_ratios["return_on_equity"] = round(roe, 2)
                        period_analysis["return_on_equity"] = analyze_roe(roe)
                    
                    if total_assets > 0:
                        roa = (net_income / total_assets) * 100
                        period_ratios["return_on_assets"] = round(roa, 2)
                        period_analysis["return_on_assets"] = analyze_roa(roa)
                    
                    if revenue > 0:
                        profit_margin = (net_income / revenue) * 100
                        operating_margin = (operating_income / revenue) * 100
                        period_ratios["profit_margin"] = round(profit_margin, 2)
                        period_ratios["operating_margin"] = round(operating_margin, 2)
                        period_analysis["profit_margin"] = analyze_profit_margin(profit_margin)
                        period_analysis["operating_margin"] = analyze_operating_margin(operating_margin)
                
                if ratio_types in ["all", "valuation"]:
                    # Valuation Ratios
                    if eps > 0:
                        pe_ratio = stock_price / eps
                        period_ratios["price_to_earnings"] = round(pe_ratio, 2)
                        period_analysis["price_to_earnings"] = analyze_pe_ratio(pe_ratio)
                    
                    if total_equity > 0 and shares_outstanding > 0:
                        book_value_per_share = total_equity / shares_outstanding
                        pb_ratio = stock_price / book_value_per_share if book_value_per_share > 0 else 0
                        period_ratios["price_to_book"] = round(pb_ratio, 2)
                        period_analysis["price_to_book"] = analyze_pb_ratio(pb_ratio)
                    
                    if revenue > 0 and market_cap > 0:
                        ps_ratio = market_cap / revenue
                        period_ratios["price_to_sales"] = round(ps_ratio, 2)
                        period_analysis["price_to_sales"] = analyze_ps_ratio(ps_ratio)
                
                if ratio_types in ["all", "liquidity"]:
                    # Liquidity Ratios
                    if current_liabilities > 0:
                        current_ratio = current_assets / current_liabilities
                        period_ratios["current_ratio"] = round(current_ratio, 2)
                        period_analysis["current_ratio"] = analyze_current_ratio(current_ratio)
                        
                        # Quick Ratio (assuming inventory is 20% of current assets as a simplification)
                        inventory = current_assets * 0.2  # Simplified approximation
                        quick_ratio = (current_assets - inventory) / current_liabilities
                        period_ratios["quick_ratio"] = round(quick_ratio, 2)
                        period_analysis["quick_ratio"] = analyze_quick_ratio(quick_ratio)
                
                if ratio_types in ["all", "solvency"]:
                    # Solvency Ratios
                    if total_equity > 0:
                        debt_to_equity = total_debt / total_equity
                        period_ratios["debt_to_equity"] = round(debt_to_equity, 2)
                        period_analysis["debt_to_equity"] = analyze_debt_to_equity(debt_to_equity)
                    
                    if operating_income > 0:
                        # Simplified interest expense calculation (assuming 5% interest rate on debt)
                        interest_expense = total_debt * 0.05
                        if interest_expense > 0:
                            interest_coverage = operating_income / interest_expense
                            period_ratios["interest_coverage"] = round(interest_coverage, 2)
                            period_analysis["interest_coverage"] = analyze_interest_coverage(interest_coverage)
                
                # Add to overall results
                ratios[period_date] = period_ratios
                analysis[period_date] = period_analysis
            
            # Prepare the final result
            result = {
                "ticker": ticker,
                "time_period": time_period,
                "ratio_types": ratio_types,
                "ratios": ratios,
                "analysis": analysis,
                "summary": generate_summary(ticker, ratios, analysis)
            }
            
            return json.dumps(result, indent=2)
        
        except Exception as e:
            logger.error(f"Error analyzing financial ratios: {str(e)}")
            return json.dumps({"error": f"Failed to analyze financial ratios: {str(e)}"}, indent=2)

    # Helper functions for ratio analysis
    def analyze_roe(roe: float) -> str:
        if roe > 20:
            return "Excellent ROE, indicating very strong profitability and efficient use of shareholder equity."
        elif roe > 15:
            return "Strong ROE, above average returns on shareholder equity."
        elif roe > 10:
            return "Good ROE, decent returns on shareholder equity."
        elif roe > 5:
            return "Average ROE, moderate returns on shareholder equity."
        else:
            return "Below average ROE, indicating potential issues with profitability or capital efficiency."
    
    def analyze_roa(roa: float) -> str:
        if roa > 10:
            return "Excellent ROA, indicating very efficient use of assets to generate profits."
        elif roa > 7:
            return "Strong ROA, above average returns on assets."
        elif roa > 5:
            return "Good ROA, decent returns on assets."
        elif roa > 3:
            return "Average ROA, moderate returns on assets."
        else:
            return "Below average ROA, indicating potential issues with asset utilization."
    
    def analyze_profit_margin(margin: float) -> str:
        if margin > 20:
            return "Excellent profit margin, indicating strong pricing power and cost control."
        elif margin > 15:
            return "Strong profit margin, above average profitability."
        elif margin > 10:
            return "Good profit margin, decent profitability."
        elif margin > 5:
            return "Average profit margin, moderate profitability."
        else:
            return "Below average profit margin, indicating potential pricing or cost issues."
    
    def analyze_operating_margin(margin: float) -> str:
        if margin > 25:
            return "Excellent operating margin, indicating very efficient operations."
        elif margin > 20:
            return "Strong operating margin, above average operational efficiency."
        elif margin > 15:
            return "Good operating margin, decent operational efficiency."
        elif margin > 10:
            return "Average operating margin, moderate operational efficiency."
        else:
            return "Below average operating margin, indicating potential operational inefficiencies."
    
    def analyze_pe_ratio(pe: float) -> str:
        if pe > 30:
            return "High P/E ratio, indicating high growth expectations or potential overvaluation."
        elif pe > 20:
            return "Above average P/E ratio, suggesting strong growth expectations."
        elif pe > 15:
            return "Average P/E ratio, in line with typical market valuations."
        elif pe > 10:
            return "Below average P/E ratio, may indicate undervaluation or expected slow growth."
        else:
            return "Low P/E ratio, suggesting potential undervaluation or concerns about future earnings."
    
    def analyze_pb_ratio(pb: float) -> str:
        if pb > 5:
            return "High P/B ratio, indicating premium valuation relative to book value."
        elif pb > 3:
            return "Above average P/B ratio, suggesting strong market confidence."
        elif pb > 2:
            return "Average P/B ratio, in line with typical market valuations."
        elif pb > 1:
            return "Below average P/B ratio, may indicate undervaluation."
        else:
            return "Low P/B ratio, suggesting potential undervaluation or concerns about asset quality."
    
    def analyze_ps_ratio(ps: float) -> str:
        if ps > 10:
            return "High P/S ratio, indicating premium valuation relative to sales."
        elif ps > 5:
            return "Above average P/S ratio, suggesting strong growth expectations."
        elif ps > 2:
            return "Average P/S ratio, in line with typical market valuations."
        elif ps > 1:
            return "Below average P/S ratio, may indicate undervaluation."
        else:
            return "Low P/S ratio, suggesting potential undervaluation or concerns about sales growth."
    
    def analyze_current_ratio(ratio: float) -> str:
        if ratio > 3:
            return "Very high current ratio, indicating strong short-term liquidity but potentially inefficient use of assets."
        elif ratio > 2:
            return "Strong current ratio, suggesting solid short-term financial health."
        elif ratio > 1.5:
            return "Good current ratio, indicating healthy short-term liquidity."
        elif ratio > 1:
            return "Adequate current ratio, suggesting sufficient short-term liquidity."
        else:
            return "Low current ratio, indicating potential short-term liquidity concerns."
    
    def analyze_quick_ratio(ratio: float) -> str:
        if ratio > 2:
            return "Very strong quick ratio, indicating excellent short-term liquidity without relying on inventory."
        elif ratio > 1.5:
            return "Strong quick ratio, suggesting solid short-term financial health."
        elif ratio > 1:
            return "Good quick ratio, indicating healthy short-term liquidity."
        elif ratio > 0.7:
            return "Adequate quick ratio, suggesting sufficient short-term liquidity."
        else:
            return "Low quick ratio, indicating potential short-term liquidity concerns."
    
    def analyze_debt_to_equity(ratio: float) -> str:
        if ratio > 2:
            return "High debt-to-equity ratio, indicating significant leverage and potential financial risk."
        elif ratio > 1.5:
            return "Above average debt-to-equity ratio, suggesting substantial leverage."
        elif ratio > 1:
            return "Moderate debt-to-equity ratio, indicating balanced use of debt financing."
        elif ratio > 0.5:
            return "Conservative debt-to-equity ratio, suggesting prudent use of leverage."
        else:
            return "Very low debt-to-equity ratio, indicating minimal financial leverage."
    
    def analyze_interest_coverage(ratio: float) -> str:
        if ratio > 8:
            return "Excellent interest coverage ratio, indicating very strong ability to meet interest obligations."
        elif ratio > 5:
            return "Strong interest coverage ratio, suggesting solid ability to service debt."
        elif ratio > 3:
            return "Good interest coverage ratio, indicating adequate ability to meet interest payments."
        elif ratio > 1.5:
            return "Adequate interest coverage ratio, suggesting sufficient ability to service debt."
        else:
            return "Low interest coverage ratio, indicating potential concerns about debt servicing ability."
    
    def generate_summary(ticker: str, ratios: Dict, analysis: Dict) -> str:
        """Generate an overall summary of the financial health based on the ratios."""
        # Get the most recent period
        if not ratios:
            return f"Insufficient data to generate a summary for {ticker}."
        
        most_recent_period = list(ratios.keys())[0]
        recent_ratios = ratios[most_recent_period]
        recent_analysis = analysis[most_recent_period]
        
        # Count strengths and weaknesses
        strengths = []
        weaknesses = []
        
        # Check profitability
        if "return_on_equity" in recent_ratios and recent_ratios["return_on_equity"] > 15:
            strengths.append("strong return on equity")
        elif "return_on_equity" in recent_ratios and recent_ratios["return_on_equity"] < 8:
            weaknesses.append("weak return on equity")
        
        if "profit_margin" in recent_ratios and recent_ratios["profit_margin"] > 15:
            strengths.append("high profit margins")
        elif "profit_margin" in recent_ratios and recent_ratios["profit_margin"] < 5:
            weaknesses.append("low profit margins")
        
        # Check liquidity
        if "current_ratio" in recent_ratios and recent_ratios["current_ratio"] > 2:
            strengths.append("strong liquidity")
        elif "current_ratio" in recent_ratios and recent_ratios["current_ratio"] < 1:
            weaknesses.append("liquidity concerns")
        
        # Check solvency
        if "debt_to_equity" in recent_ratios and recent_ratios["debt_to_equity"] < 0.5:
            strengths.append("low leverage")
        elif "debt_to_equity" in recent_ratios and recent_ratios["debt_to_equity"] > 2:
            weaknesses.append("high leverage")
        
        # Check valuation
        if "price_to_earnings" in recent_ratios:
            pe = recent_ratios["price_to_earnings"]
            if pe < 15:
                strengths.append("potentially undervalued (low P/E)")
            elif pe > 30:
                weaknesses.append("potentially overvalued (high P/E)")
        
        # Generate summary text
        summary = f"Financial analysis for {ticker} as of {most_recent_period}: "
        
        if strengths and weaknesses:
            summary += f"The company shows {', '.join(strengths)}, but has {', '.join(weaknesses)}."
        elif strengths:
            summary += f"The company demonstrates financial strength with {', '.join(strengths)}."
        elif weaknesses:
            summary += f"The company faces financial challenges including {', '.join(weaknesses)}."
        else:
            summary += "The company shows mixed financial indicators with no standout strengths or weaknesses."
        
        return summary

    # Add a resource
    @server.resource("history://financial-data")
    def financial_data_info() -> str:
        """Information about financial datasets and their usage."""
        return (
            "Financial Datasets API provides comprehensive financial data including "
            "income statements, balance sheets, cash flow statements, stock prices, "
            "crypto prices, and SEC filings for public companies. "
            "The data is sourced from public financial reports and market data providers."
        )

    return server
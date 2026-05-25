"""
Alpha Vantage API Service for real-time market data and financial analysis.
Provides stock prices, forex, commodities, economic indicators, and more.
"""
import requests
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json


class AlphaVantageService:
    """Service for interacting with Alpha Vantage API."""
    
    def __init__(self, api_key: str):
        """
        Initialize Alpha Vantage service.
        
        Args:
            api_key: Alpha Vantage API key
        """
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    def _make_request(self, params: Dict) -> Dict:
        """
        Make API request to Alpha Vantage.
        
        Args:
            params: Request parameters
        
        Returns:
            API response data
        """
        params['apikey'] = self.api_key
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
    
    # ==================== STOCK DATA ====================
    
    def get_stock_quote(self, symbol: str) -> Dict:
        """
        Get real-time stock quote.
        
        Args:
            symbol: Stock symbol (e.g., 'XOM' for ExxonMobil)
        
        Returns:
            Current stock price and details
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }
        data = self._make_request(params)
        
        if 'Global Quote' in data:
            quote = data['Global Quote']
            return {
                'symbol': quote.get('01. symbol'),
                'price': float(quote.get('05. price', 0)),
                'change': float(quote.get('09. change', 0)),
                'change_percent': quote.get('10. change percent', '0%'),
                'volume': int(quote.get('06. volume', 0)),
                'latest_trading_day': quote.get('07. latest trading day'),
                'previous_close': float(quote.get('08. previous close', 0)),
                'open': float(quote.get('02. open', 0)),
                'high': float(quote.get('03. high', 0)),
                'low': float(quote.get('04. low', 0))
            }
        return {}
    
    def get_stock_daily(self, symbol: str, outputsize: str = 'compact') -> pd.DataFrame:
        """
        Get daily stock prices.
        
        Args:
            symbol: Stock symbol
            outputsize: 'compact' (100 days) or 'full' (20+ years)
        
        Returns:
            DataFrame with daily prices
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': outputsize
        }
        data = self._make_request(params)
        
        if 'Time Series (Daily)' in data:
            df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
            df.index = pd.to_datetime(df.index)
            df.columns = ['open', 'high', 'low', 'close', 'volume']
            df = df.astype(float)
            return df.sort_index()
        return pd.DataFrame()
    
    def get_stock_intraday(self, symbol: str, interval: str = '5min') -> pd.DataFrame:
        """
        Get intraday stock prices.
        
        Args:
            symbol: Stock symbol
            interval: '1min', '5min', '15min', '30min', '60min'
        
        Returns:
            DataFrame with intraday prices
        """
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval
        }
        data = self._make_request(params)
        
        key = f'Time Series ({interval})'
        if key in data:
            df = pd.DataFrame.from_dict(data[key], orient='index')
            df.index = pd.to_datetime(df.index)
            df.columns = ['open', 'high', 'low', 'close', 'volume']
            df = df.astype(float)
            return df.sort_index()
        return pd.DataFrame()
    
    def search_symbol(self, keywords: str) -> List[Dict]:
        """
        Search for stock symbols.
        
        Args:
            keywords: Search keywords (company name, symbol)
        
        Returns:
            List of matching symbols
        """
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords
        }
        data = self._make_request(params)
        
        if 'bestMatches' in data:
            return [
                {
                    'symbol': match['1. symbol'],
                    'name': match['2. name'],
                    'type': match['3. type'],
                    'region': match['4. region'],
                    'currency': match['8. currency']
                }
                for match in data['bestMatches']
            ]
        return []
    
    # ==================== COMPANY FUNDAMENTALS ====================
    
    def get_company_overview(self, symbol: str) -> Dict:
        """
        Get comprehensive company information.
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Company fundamentals and metrics
        """
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }
        data = self._make_request(params)
        
        if data and 'Symbol' in data:
            return {
                'symbol': data.get('Symbol'),
                'name': data.get('Name'),
                'description': data.get('Description'),
                'sector': data.get('Sector'),
                'industry': data.get('Industry'),
                'market_cap': float(data.get('MarketCapitalization', 0)),
                'pe_ratio': float(data.get('PERatio', 0)),
                'peg_ratio': float(data.get('PEGRatio', 0)),
                'book_value': float(data.get('BookValue', 0)),
                'dividend_yield': float(data.get('DividendYield', 0)),
                'eps': float(data.get('EPS', 0)),
                'revenue_per_share': float(data.get('RevenuePerShareTTM', 0)),
                'profit_margin': float(data.get('ProfitMargin', 0)),
                'operating_margin': float(data.get('OperatingMarginTTM', 0)),
                'roe': float(data.get('ReturnOnEquityTTM', 0)),
                'roa': float(data.get('ReturnOnAssetsTTM', 0)),
                'beta': float(data.get('Beta', 0)),
                '52_week_high': float(data.get('52WeekHigh', 0)),
                '52_week_low': float(data.get('52WeekLow', 0)),
                'analyst_target_price': float(data.get('AnalystTargetPrice', 0))
            }
        return {}
    
    def get_income_statement(self, symbol: str) -> List[Dict]:
        """
        Get company income statements.
        
        Args:
            symbol: Stock symbol
        
        Returns:
            List of annual income statements
        """
        params = {
            'function': 'INCOME_STATEMENT',
            'symbol': symbol
        }
        data = self._make_request(params)
        
        if 'annualReports' in data:
            return data['annualReports']
        return []
    
    def get_balance_sheet(self, symbol: str) -> List[Dict]:
        """
        Get company balance sheets.
        
        Args:
            symbol: Stock symbol
        
        Returns:
            List of annual balance sheets
        """
        params = {
            'function': 'BALANCE_SHEET',
            'symbol': symbol
        }
        data = self._make_request(params)
        
        if 'annualReports' in data:
            return data['annualReports']
        return []
    
    def get_cash_flow(self, symbol: str) -> List[Dict]:
        """
        Get company cash flow statements.
        
        Args:
            symbol: Stock symbol
        
        Returns:
            List of annual cash flow statements
        """
        params = {
            'function': 'CASH_FLOW',
            'symbol': symbol
        }
        data = self._make_request(params)
        
        if 'annualReports' in data:
            return data['annualReports']
        return []
    
    def get_earnings(self, symbol: str) -> Dict:
        """
        Get company earnings data.
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Earnings history and estimates
        """
        params = {
            'function': 'EARNINGS',
            'symbol': symbol
        }
        return self._make_request(params)
    
    # ==================== COMMODITIES & FOREX ====================
    
    def get_crude_oil_wti(self, interval: str = 'monthly') -> pd.DataFrame:
        """
        Get WTI Crude Oil prices.
        
        Args:
            interval: 'daily', 'weekly', 'monthly'
        
        Returns:
            DataFrame with oil prices
        """
        params = {
            'function': 'WTI',
            'interval': interval
        }
        data = self._make_request(params)
        
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = df['value'].astype(float)
            df = df.set_index('date').sort_index()
            return df
        return pd.DataFrame()
    
    def get_crude_oil_brent(self, interval: str = 'monthly') -> pd.DataFrame:
        """
        Get Brent Crude Oil prices.
        
        Args:
            interval: 'daily', 'weekly', 'monthly'
        
        Returns:
            DataFrame with oil prices
        """
        params = {
            'function': 'BRENT',
            'interval': interval
        }
        data = self._make_request(params)
        
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = df['value'].astype(float)
            df = df.set_index('date').sort_index()
            return df
        return pd.DataFrame()
    
    def get_natural_gas(self, interval: str = 'monthly') -> pd.DataFrame:
        """
        Get Natural Gas prices.
        
        Args:
            interval: 'daily', 'weekly', 'monthly'
        
        Returns:
            DataFrame with natural gas prices
        """
        params = {
            'function': 'NATURAL_GAS',
            'interval': interval
        }
        data = self._make_request(params)
        
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = df['value'].astype(float)
            df = df.set_index('date').sort_index()
            return df
        return pd.DataFrame()
    
    def get_forex_rate(self, from_currency: str, to_currency: str) -> Dict:
        """
        Get real-time forex exchange rate.
        
        Args:
            from_currency: From currency code (e.g., 'USD')
            to_currency: To currency code (e.g., 'EUR')
        
        Returns:
            Exchange rate data
        """
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': from_currency,
            'to_currency': to_currency
        }
        data = self._make_request(params)
        
        if 'Realtime Currency Exchange Rate' in data:
            rate = data['Realtime Currency Exchange Rate']
            return {
                'from': rate.get('1. From_Currency Code'),
                'to': rate.get('3. To_Currency Code'),
                'rate': float(rate.get('5. Exchange Rate', 0)),
                'last_refreshed': rate.get('6. Last Refreshed'),
                'bid': float(rate.get('8. Bid Price', 0)),
                'ask': float(rate.get('9. Ask Price', 0))
            }
        return {}
    
    # ==================== ECONOMIC INDICATORS ====================
    
    def get_real_gdp(self, interval: str = 'annual') -> pd.DataFrame:
        """
        Get US Real GDP data.
        
        Args:
            interval: 'annual' or 'quarterly'
        
        Returns:
            DataFrame with GDP data
        """
        params = {
            'function': 'REAL_GDP',
            'interval': interval
        }
        data = self._make_request(params)
        
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = df['value'].astype(float)
            df = df.set_index('date').sort_index()
            return df
        return pd.DataFrame()
    
    def get_inflation(self) -> pd.DataFrame:
        """
        Get US inflation rate (CPI).
        
        Returns:
            DataFrame with inflation data
        """
        params = {
            'function': 'INFLATION'
        }
        data = self._make_request(params)
        
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = df['value'].astype(float)
            df = df.set_index('date').sort_index()
            return df
        return pd.DataFrame()
    
    def get_unemployment_rate(self) -> pd.DataFrame:
        """
        Get US unemployment rate.
        
        Returns:
            DataFrame with unemployment data
        """
        params = {
            'function': 'UNEMPLOYMENT'
        }
        data = self._make_request(params)
        
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = df['value'].astype(float)
            df = df.set_index('date').sort_index()
            return df
        return pd.DataFrame()
    
    def get_federal_funds_rate(self, interval: str = 'monthly') -> pd.DataFrame:
        """
        Get Federal Funds Rate.
        
        Args:
            interval: 'daily', 'weekly', 'monthly'
        
        Returns:
            DataFrame with interest rate data
        """
        params = {
            'function': 'FEDERAL_FUNDS_RATE',
            'interval': interval
        }
        data = self._make_request(params)
        
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = df['value'].astype(float)
            df = df.set_index('date').sort_index()
            return df
        return pd.DataFrame()
    
    # ==================== TECHNICAL INDICATORS ====================
    
    def get_sma(self, symbol: str, interval: str = 'daily', 
                time_period: int = 50, series_type: str = 'close') -> pd.DataFrame:
        """
        Get Simple Moving Average.
        
        Args:
            symbol: Stock symbol
            interval: Time interval
            time_period: Number of periods
            series_type: 'close', 'open', 'high', 'low'
        
        Returns:
            DataFrame with SMA values
        """
        params = {
            'function': 'SMA',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': series_type
        }
        data = self._make_request(params)
        
        if 'Technical Analysis: SMA' in data:
            df = pd.DataFrame.from_dict(data['Technical Analysis: SMA'], orient='index')
            df.index = pd.to_datetime(df.index)
            df.columns = ['SMA']
            df = df.astype(float)
            return df.sort_index()
        return pd.DataFrame()
    
    def get_rsi(self, symbol: str, interval: str = 'daily', 
                time_period: int = 14, series_type: str = 'close') -> pd.DataFrame:
        """
        Get Relative Strength Index.
        
        Args:
            symbol: Stock symbol
            interval: Time interval
            time_period: Number of periods
            series_type: 'close', 'open', 'high', 'low'
        
        Returns:
            DataFrame with RSI values
        """
        params = {
            'function': 'RSI',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': series_type
        }
        data = self._make_request(params)
        
        if 'Technical Analysis: RSI' in data:
            df = pd.DataFrame.from_dict(data['Technical Analysis: RSI'], orient='index')
            df.index = pd.to_datetime(df.index)
            df.columns = ['RSI']
            df = df.astype(float)
            return df.sort_index()
        return pd.DataFrame()
    
    # ==================== ADVANCED ANALYSIS ====================
    
    def analyze_oil_gas_company(self, symbol: str) -> Dict:
        """
        Comprehensive analysis of oil & gas company.
        
        Args:
            symbol: Stock symbol (e.g., 'XOM', 'CVX', 'COP')
        
        Returns:
            Complete company analysis
        """
        try:
            # Get all data
            overview = self.get_company_overview(symbol)
            quote = self.get_stock_quote(symbol)
            daily_prices = self.get_stock_daily(symbol, 'compact')
            
            # Calculate metrics
            if not daily_prices.empty:
                returns = daily_prices['close'].pct_change()
                volatility = returns.std() * (252 ** 0.5)  # Annualized
                
                # Price trends
                price_52w_high = daily_prices['high'].max()
                price_52w_low = daily_prices['low'].min()
                current_price = quote.get('price', 0)
                
                # Performance
                perf_1m = ((current_price / daily_prices['close'].iloc[-21]) - 1) * 100 if len(daily_prices) > 21 else 0
                perf_3m = ((current_price / daily_prices['close'].iloc[-63]) - 1) * 100 if len(daily_prices) > 63 else 0
                perf_ytd = ((current_price / daily_prices['close'].iloc[0]) - 1) * 100
            else:
                volatility = 0
                price_52w_high = 0
                price_52w_low = 0
                perf_1m = 0
                perf_3m = 0
                perf_ytd = 0
            
            return {
                'symbol': symbol,
                'company_info': overview,
                'current_quote': quote,
                'metrics': {
                    'volatility': volatility,
                    '52_week_high': price_52w_high,
                    '52_week_low': price_52w_low,
                    'performance_1m': perf_1m,
                    'performance_3m': perf_3m,
                    'performance_ytd': perf_ytd
                },
                'valuation': {
                    'pe_ratio': overview.get('pe_ratio', 0),
                    'peg_ratio': overview.get('peg_ratio', 0),
                    'book_value': overview.get('book_value', 0),
                    'market_cap': overview.get('market_cap', 0)
                },
                'profitability': {
                    'profit_margin': overview.get('profit_margin', 0),
                    'operating_margin': overview.get('operating_margin', 0),
                    'roe': overview.get('roe', 0),
                    'roa': overview.get('roa', 0)
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_market_context(self) -> Dict:
        """
        Get comprehensive market context for M&A analysis.
        
        Returns:
            Market indicators and commodity prices
        """
        try:
            # Get commodity prices
            wti_oil = self.get_crude_oil_wti('monthly')
            brent_oil = self.get_crude_oil_brent('monthly')
            nat_gas = self.get_natural_gas('monthly')
            
            # Get economic indicators
            gdp = self.get_real_gdp('quarterly')
            inflation = self.get_inflation()
            unemployment = self.get_unemployment_rate()
            fed_rate = self.get_federal_funds_rate('monthly')
            
            return {
                'commodities': {
                    'wti_oil': {
                        'current': float(wti_oil['value'].iloc[-1]) if not wti_oil.empty else 0,
                        'avg_12m': float(wti_oil['value'].tail(12).mean()) if not wti_oil.empty else 0,
                        'trend': 'up' if not wti_oil.empty and wti_oil['value'].iloc[-1] > wti_oil['value'].iloc[-2] else 'down'
                    },
                    'brent_oil': {
                        'current': float(brent_oil['value'].iloc[-1]) if not brent_oil.empty else 0,
                        'avg_12m': float(brent_oil['value'].tail(12).mean()) if not brent_oil.empty else 0
                    },
                    'natural_gas': {
                        'current': float(nat_gas['value'].iloc[-1]) if not nat_gas.empty else 0,
                        'avg_12m': float(nat_gas['value'].tail(12).mean()) if not nat_gas.empty else 0
                    }
                },
                'economic_indicators': {
                    'gdp_growth': float(gdp['value'].iloc[-1]) if not gdp.empty else 0,
                    'inflation_rate': float(inflation['value'].iloc[-1]) if not inflation.empty else 0,
                    'unemployment_rate': float(unemployment['value'].iloc[-1]) if not unemployment.empty else 0,
                    'fed_funds_rate': float(fed_rate['value'].iloc[-1]) if not fed_rate.empty else 0
                },
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}


# Global instance
alpha_vantage_service = None

def get_alpha_vantage_service(api_key: str) -> AlphaVantageService:
    """Get or create Alpha Vantage service instance."""
    global alpha_vantage_service
    if alpha_vantage_service is None:
        alpha_vantage_service = AlphaVantageService(api_key)
    return alpha_vantage_service

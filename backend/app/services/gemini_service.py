"""
Google Gemini AI Service for intelligent analysis and suggestions.
Enhanced with Alpha Vantage for real-time market data.
"""
import os
import json
import pandas as pd
import io
from typing import Dict, List, Optional
import google.generativeai as genai
from decimal import Decimal
from datetime import datetime


class GeminiService:
    """Service for interacting with Google Gemini AI."""
    
    def __init__(self, api_key: str, alpha_vantage_key: Optional[str] = None):
        """
        Initialize Gemini service with optional Alpha Vantage integration.
        
        Args:
            api_key: Google Gemini API key
            alpha_vantage_key: Alpha Vantage API key (optional)
        """
        self.api_key = api_key
        self.alpha_vantage_key = alpha_vantage_key
        self.alpha_vantage = None
        self.web_scraper = None
        
        # Initialize Alpha Vantage if key provided
        if alpha_vantage_key:
            try:
                from app.services.alpha_vantage_service import AlphaVantageService
                self.alpha_vantage = AlphaVantageService(alpha_vantage_key)
            except Exception as e:
                print(f"Alpha Vantage initialization failed: {e}")
        
        # Initialize Web Scraper
        try:
            from app.services.web_scraper_service import WebScraperService
            self.web_scraper = WebScraperService()
        except Exception as e:
            print(f"Web Scraper initialization failed: {e}")
        
        genai.configure(api_key=api_key)
        # Use the latest Gemini model with enhanced configuration for better responses
        generation_config = {
            'temperature': 0.7,  # Balanced creativity and accuracy
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 8192,  # Allow longer, more detailed responses
        }
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=generation_config
        )
        self.chat = None
    
    def start_chat(self, context: Optional[str] = None) -> None:
        """
        Start a new chat session with enhanced system prompt.
        
        Args:
            context: Optional context to initialize the chat
        """
        # Enhanced system prompt for better responses
        system_prompt = """You are an expert Oil & Gas M&A Advisor with 20+ years of experience in:
        - Upstream asset valuation and acquisition
        - Reserve engineering and decline curve analysis
        - Financial modeling (DCF, NPV, IRR)
        - Due diligence and risk assessment
        - Deal structuring and negotiation
        - Synergy identification and quantification
        
        Your responses should be:
        1. **Detailed and Comprehensive** - Provide thorough explanations with specific examples
        2. **Easy to Understand** - Use clear language, bullet points, and structured formatting
        3. **Actionable** - Give specific recommendations with numbers and steps
        4. **Professional** - Use industry terminology but explain complex concepts
        5. **Practical** - Focus on real-world application and implementation
        
        Always structure your responses with:
        - Clear headings and sections
        - Bullet points for lists
        - Specific numbers and ranges
        - Examples when helpful
        - Next steps or action items
        
        Be conversational yet professional, like a trusted advisor explaining to a colleague."""
        
        history = []
        if context:
            full_context = f"{system_prompt}\n\n{context}"
            history.append({
                'role': 'user',
                'parts': [full_context]
            })
            history.append({
                'role': 'model',
                'parts': ['Understood! I\'m ready to provide detailed, actionable advice on oil & gas M&A valuation. I\'ll make sure my responses are comprehensive, easy to understand, and practical. What would you like to discuss?']
            })
        else:
            history.append({
                'role': 'user',
                'parts': [system_prompt]
            })
            history.append({
                'role': 'model',
                'parts': ['Perfect! I\'m your expert M&A advisor ready to help with detailed analysis and recommendations. Ask me anything about valuations, assumptions, risks, synergies, or deal structuring!']
            })
        
        self.chat = self.model.start_chat(history=history)
    
    def send_message(self, message: str) -> str:
        """
        Send a message to the AI and get response.
        
        Args:
            message: User message
        
        Returns:
            AI response
        """
        if not self.chat:
            self.start_chat()
        
        response = self.chat.send_message(message)
        return response.text
    
    def analyze_project(self, project_data: Dict) -> Dict:
        """
        Analyze a project and provide comprehensive AI insights.
        
        Args:
            project_data: Project information
        
        Returns:
            Analysis results with detailed suggestions
        """
        prompt = f"""
        As an expert M&A advisor, provide a COMPREHENSIVE analysis of this oil & gas project:
        
        **Project Details:**
        - Name: {project_data.get('name')}
        - Type: {project_data.get('project_type')}
        - Deal Size: ${project_data.get('deal_size', 0):,.0f}
        - Description: {project_data.get('description', 'N/A')}
        
        Provide a DETAILED analysis covering:
        
        ## 1. KEY RISKS (List 5-7 specific risks with mitigation strategies)
        For each risk, explain:
        - What the risk is
        - Why it matters
        - How to mitigate it
        
        ## 2. RECOMMENDED ASSUMPTIONS
        Provide specific numbers with reasoning:
        - Decline Rate: X% (explain why)
        - Discount Rate: Y% (explain why)
        - Forecast Period: Z years (explain why)
        - Oil Price Assumptions
        - Gas Price Assumptions
        
        ## 3. SYNERGY OPPORTUNITIES (List 4-6 specific synergies)
        For each synergy:
        - Category (cost/revenue/tax/financial)
        - Specific description
        - Estimated annual value ($)
        - Timeline to realize
        - Confidence level
        
        ## 4. DEAL STRUCTURE RECOMMENDATIONS
        Suggest:
        - Payment structure (cash/stock/earnout)
        - Timing considerations
        - Contingencies to include
        - Tax optimization strategies
        
        ## 5. DUE DILIGENCE PRIORITIES (Top 8-10 items)
        List specific items to verify:
        - Technical due diligence
        - Financial due diligence
        - Legal/regulatory
        - Environmental
        - Operational
        
        Make your response DETAILED, SPECIFIC, and ACTIONABLE. Use real numbers and examples.
        Format as JSON with keys: risks, assumptions, synergies, deal_structure, due_diligence, executive_summary
        """
        
        response = self.model.generate_content(prompt)
        
        try:
            # Try to parse as JSON
            result = json.loads(response.text)
        except:
            # If not JSON, structure the response
            result = {
                'analysis': response.text,
                'risks': ['Review the full analysis for detailed risks'],
                'assumptions': {'decline_rate': 0.15, 'discount_rate': 0.12},
                'synergies': ['Operational efficiencies', 'Cost synergies'],
                'deal_structure': 'Review the full analysis',
                'due_diligence': ['Production data verification', 'Reserve audit']
            }
        
        return result
    
    def optimize_assumptions(self, project_data: Dict, historical_data: Dict) -> Dict:
        """
        Use AI to optimize modeling assumptions based on data.
        
        Args:
            project_data: Project information
            historical_data: Historical production and financial data
        
        Returns:
            Optimized assumptions
        """
        prompt = f"""
        Based on this oil & gas project data, recommend optimal modeling assumptions:
        
        Project Type: {project_data.get('project_type')}
        Deal Size: ${project_data.get('deal_size', 0):,.0f}
        
        Historical Data Summary:
        - Production records: {historical_data.get('production_count', 0)}
        - Financial records: {historical_data.get('financial_count', 0)}
        - Average oil production: {historical_data.get('avg_oil', 0):.0f} bbl/day
        - Average gas production: {historical_data.get('avg_gas', 0):.0f} MCF/day
        
        Recommend:
        1. Decline curve type (exponential, hyperbolic, harmonic)
        2. Decline rate (0.10 to 0.25)
        3. Discount rate (0.10 to 0.15)
        4. Forecast years (10 to 30)
        5. Exit multiple (4.0 to 7.0)
        
        Provide as JSON with keys: decline_curve_type, decline_rate, discount_rate, forecast_years, exit_multiple, reasoning
        """
        
        response = self.model.generate_content(prompt)
        
        try:
            result = json.loads(response.text)
        except:
            # Default recommendations
            result = {
                'decline_curve_type': 'exponential',
                'decline_rate': 0.15,
                'discount_rate': 0.12,
                'forecast_years': 20,
                'exit_multiple': 5.0,
                'reasoning': response.text
            }
        
        return result
    
    def analyze_valuation_results(self, results: Dict) -> Dict:
        """
        Analyze valuation results and provide investment recommendation.
        
        Args:
            results: Valuation results
        
        Returns:
            Analysis and recommendation
        """
        metrics = results.get('metrics', {})
        
        prompt = f"""
        Analyze these oil & gas M&A valuation results and provide investment recommendation:
        
        Valuation Metrics:
        - NPV: ${metrics.get('npv', 0):,.0f}
        - IRR: {metrics.get('irr', 0):.1f}%
        - Payback Period: {metrics.get('payback_period', 0):.1f} years
        - ROIC: {metrics.get('roic', 0):.1f}%
        - Terminal Value: ${metrics.get('terminal_value', 0):,.0f}
        
        Scenario: {results.get('scenario_name')}
        Type: {results.get('scenario_type')}
        
        Provide:
        1. Investment recommendation (Strong Buy, Buy, Hold, Sell, Strong Sell)
        2. Key strengths
        3. Key concerns
        4. Sensitivity factors to monitor
        5. Suggested price range
        
        Format as JSON with keys: recommendation, rating, strengths, concerns, sensitivities, price_range
        """
        
        response = self.model.generate_content(prompt)
        
        try:
            result = json.loads(response.text)
        except:
            # Provide basic recommendation
            npv = metrics.get('npv', 0)
            irr = metrics.get('irr', 0)
            
            if npv > 0 and irr > 12:
                recommendation = 'Buy'
                rating = 4
            elif npv > 0:
                recommendation = 'Hold'
                rating = 3
            else:
                recommendation = 'Sell'
                rating = 2
            
            result = {
                'recommendation': recommendation,
                'rating': rating,
                'analysis': response.text,
                'strengths': ['Positive NPV'] if npv > 0 else [],
                'concerns': ['Negative NPV'] if npv <= 0 else [],
                'sensitivities': ['Oil price', 'Decline rate', 'Discount rate'],
                'price_range': 'See full analysis'
            }
        
        return result
    
    def suggest_synergies(self, project_data: Dict, assumptions: Dict) -> List[Dict]:
        """
        Use AI to suggest potential synergies.
        
        Args:
            project_data: Project information
            assumptions: Current assumptions
        
        Returns:
            List of suggested synergies
        """
        prompt = f"""
        Suggest realistic synergies for this oil & gas M&A deal:
        
        Project Type: {project_data.get('project_type')}
        Deal Size: ${project_data.get('deal_size', 0):,.0f}
        
        Suggest 3-5 synergies with:
        1. Category (cost_synergies, revenue_synergies, tax_synergies, financial_synergies)
        2. Description
        3. Target annual value ($)
        4. Realization timeline (years)
        5. Confidence level (high, medium, low)
        
        Format as JSON array with objects containing: category, description, target_value, years, confidence
        """
        
        response = self.model.generate_content(prompt)
        
        try:
            result = json.loads(response.text)
            if not isinstance(result, list):
                result = result.get('synergies', [])
        except:
            # Default synergies
            deal_size = project_data.get('deal_size', 50000000)
            result = [
                {
                    'category': 'cost_synergies',
                    'description': 'Operational efficiencies and overhead reduction',
                    'target_value': deal_size * 0.02,  # 2% of deal size
                    'years': 3,
                    'confidence': 'high'
                },
                {
                    'category': 'revenue_synergies',
                    'description': 'Enhanced production optimization',
                    'target_value': deal_size * 0.01,  # 1% of deal size
                    'years': 5,
                    'confidence': 'medium'
                }
            ]
        
        return result
    
    def compare_scenarios(self, scenarios: List[Dict]) -> Dict:
        """
        Compare multiple scenarios and provide recommendation.
        
        Args:
            scenarios: List of scenario results
        
        Returns:
            Comparison analysis
        """
        scenarios_text = "\n".join([
            f"{s['scenario_name']}: NPV ${s['metrics']['npv']:,.0f}, IRR {s['metrics']['irr']:.1f}%"
            for s in scenarios
        ])
        
        prompt = f"""
        Compare these valuation scenarios and provide recommendation:
        
        {scenarios_text}
        
        Provide:
        1. Best case analysis
        2. Worst case analysis
        3. Most likely outcome
        4. Risk assessment
        5. Final recommendation
        
        Format as JSON with keys: best_case, worst_case, likely_outcome, risk_level, recommendation
        """
        
        response = self.model.generate_content(prompt)
        
        try:
            result = json.loads(response.text)
        except:
            result = {
                'analysis': response.text,
                'best_case': scenarios[0]['scenario_name'] if scenarios else 'N/A',
                'worst_case': scenarios[-1]['scenario_name'] if scenarios else 'N/A',
                'likely_outcome': 'Base case',
                'risk_level': 'Medium',
                'recommendation': 'Proceed with caution'
            }
        
        return result
    
    def chat_about_project(self, message: str, project_context: Dict) -> str:
        """
        Chat with AI about a specific project with enhanced responses.
        
        Args:
            message: User message
            project_context: Project information for context
        
        Returns:
            Detailed, user-friendly AI response
        """
        if not self.chat:
            context = f"""
            You are analyzing this specific oil & gas M&A project:
            
            **Project Details:**
            - Name: {project_context.get('name')}
            - Type: {project_context.get('project_type')}
            - Deal Size: ${project_context.get('deal_size', 0):,.0f}
            - Description: {project_context.get('description', 'N/A')}
            
            For every question, provide:
            1. **Clear Answer** - Direct response to the question
            2. **Detailed Explanation** - Why this matters and how it works
            3. **Specific Numbers** - Ranges, percentages, dollar amounts
            4. **Examples** - Real-world scenarios when helpful
            5. **Action Steps** - What to do next
            6. **Considerations** - Things to watch out for
            
            Use formatting:
            - **Bold** for key points
            - Bullet points for lists
            - Numbers for steps
            - Clear sections with headings
            
            Make responses comprehensive (200-400 words) but easy to read and understand.
            """
            self.start_chat(context)
        
        # Enhance the user's message with instructions for better responses
        enhanced_message = f"""
        {message}
        
        Please provide a DETAILED, COMPREHENSIVE response that:
        - Explains concepts clearly for easy understanding
        - Includes specific numbers, ranges, and examples
        - Uses bullet points and formatting for readability
        - Gives actionable recommendations
        - Covers all relevant aspects of the question
        """
        
        return self.send_message(enhanced_message)
    
    def analyze_csv_data(self, csv_content: str, filename: str) -> Dict:
        """
        Analyze CSV data and provide comprehensive insights.
        
        Args:
            csv_content: CSV file content as string
            filename: Name of the CSV file
        
        Returns:
            Analysis results with detailed insights
        """
        try:
            # Parse CSV
            df = pd.read_csv(io.StringIO(csv_content))
            
            # Get basic statistics
            stats = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'data_types': df.dtypes.astype(str).to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'sample_data': df.head(5).to_dict('records')
            }
            
            # Get numeric column statistics
            numeric_stats = {}
            for col in df.select_dtypes(include=['number']).columns:
                numeric_stats[col] = {
                    'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                    'median': float(df[col].median()) if not df[col].isna().all() else None,
                    'min': float(df[col].min()) if not df[col].isna().all() else None,
                    'max': float(df[col].max()) if not df[col].isna().all() else None,
                    'std': float(df[col].std()) if not df[col].isna().all() else None
                }
            
            # Create enhanced prompt for detailed AI analysis
            prompt = f"""
            As an expert data analyst for oil & gas M&A, provide a COMPREHENSIVE analysis of this CSV file:
            
            **File Information:**
            - Filename: {filename}
            - Total Rows: {stats['rows']:,}
            - Total Columns: {stats['columns']}
            - Column Names: {', '.join(stats['column_names'])}
            
            **Numeric Statistics:**
            {json.dumps(numeric_stats, indent=2)}
            
            **Sample Data (First 5 Rows):**
            {json.dumps(stats['sample_data'], indent=2)}
            
            **Missing Values:**
            {json.dumps(stats['missing_values'], indent=2)}
            
            Provide a DETAILED analysis with these sections:
            
            ## 1. DATA TYPE IDENTIFICATION
            - What type of data is this? (production, financial, reserve, well data, etc.)
            - What time period does it cover?
            - What assets or wells are included?
            
            ## 2. DATA QUALITY ASSESSMENT
            - Overall quality rating (Excellent/Good/Fair/Poor)
            - Completeness (% of missing data)
            - Consistency issues
            - Outliers or anomalies detected
            
            ## 3. KEY INSIGHTS & PATTERNS
            - Trends over time (if applicable)
            - Performance metrics
            - Notable patterns or correlations
            - Comparison to industry benchmarks
            
            ## 4. VALUATION IMPLICATIONS
            - How this data impacts valuation
            - Key metrics to focus on
            - Assumptions this data supports
            - Risks or concerns identified
            
            ## 5. RED FLAGS & CONCERNS
            - Data quality issues
            - Suspicious patterns
            - Missing critical information
            - Inconsistencies to investigate
            
            ## 6. RECOMMENDATIONS
            - How to use this data in valuation model
            - Additional data needed
            - Verification steps required
            - Next actions to take
            
            ## 7. SPECIFIC NUMBERS & METRICS
            - Calculate key ratios
            - Identify trends (% change)
            - Highlight important values
            
            Make your analysis DETAILED (300-500 words), SPECIFIC with numbers, and ACTIONABLE.
            Use **bold** for key points and bullet points for clarity.
            """
            
            response = self.model.generate_content(prompt)
            
            return {
                'success': True,
                'filename': filename,
                'statistics': stats,
                'numeric_statistics': numeric_stats,
                'ai_analysis': response.text,
                'data_preview': stats['sample_data']
            }
        
        except Exception as e:
            return {
                'success': False,
                'filename': filename,
                'error': str(e),
                'message': 'Failed to analyze CSV file. Please check the file format.'
            }
    
    def generate_report_summary(self, project_data: Dict, valuation_results: Dict) -> str:
        """
        Generate an executive summary report.
        
        Args:
            project_data: Project information
            valuation_results: Valuation results
        
        Returns:
            Executive summary text
        """
        metrics = valuation_results.get('metrics', {})
        
        prompt = f"""
        Generate a professional executive summary for this M&A valuation:
        
        Project: {project_data.get('name')}
        Type: {project_data.get('project_type')}
        Deal Size: ${project_data.get('deal_size', 0):,.0f}
        
        Valuation Results:
        - NPV: ${metrics.get('npv', 0):,.0f}
        - IRR: {metrics.get('irr', 0):.1f}%
        - Payback: {metrics.get('payback_period', 0):.1f} years
        - ROIC: {metrics.get('roic', 0):.1f}%
        
        Create a 3-paragraph executive summary covering:
        1. Transaction overview
        2. Financial analysis
        3. Recommendation
        
        Professional, concise, investment-committee ready.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    # ==================== ALPHA VANTAGE INTEGRATION ====================
    
    def analyze_with_market_data(self, message: str, include_commodities: bool = True,
                                 include_companies: Optional[List[str]] = None) -> str:
        """
        Analyze with real-time market data from Alpha Vantage.
        
        Args:
            message: User question/request
            include_commodities: Include oil & gas prices
            include_companies: List of company symbols to analyze
        
        Returns:
            AI analysis with real-time market context
        """
        if not self.alpha_vantage:
            return self.send_message(message)
        
        try:
            # Get market context
            market_data = []
            
            if include_commodities:
                # Get oil & gas prices
                try:
                    wti = self.alpha_vantage.get_crude_oil_wti('monthly')
                    if not wti.empty:
                        current_wti = float(wti['value'].iloc[-1])
                        avg_wti = float(wti['value'].tail(12).mean())
                        market_data.append(f"**WTI Crude Oil:** ${current_wti:.2f}/bbl (12-month avg: ${avg_wti:.2f}/bbl)")
                except:
                    pass
                
                try:
                    brent = self.alpha_vantage.get_crude_oil_brent('monthly')
                    if not brent.empty:
                        current_brent = float(brent['value'].iloc[-1])
                        market_data.append(f"**Brent Crude:** ${current_brent:.2f}/bbl")
                except:
                    pass
                
                try:
                    gas = self.alpha_vantage.get_natural_gas('monthly')
                    if not gas.empty:
                        current_gas = float(gas['value'].iloc[-1])
                        market_data.append(f"**Natural Gas:** ${current_gas:.2f}/MMBtu")
                except:
                    pass
            
            if include_companies:
                # Get company data
                for symbol in include_companies[:3]:  # Limit to 3 companies
                    try:
                        quote = self.alpha_vantage.get_stock_quote(symbol)
                        if quote:
                            market_data.append(
                                f"**{symbol}:** ${quote['price']:.2f} ({quote['change_percent']})"
                            )
                    except:
                        pass
            
            # Create enhanced prompt with market data
            market_context = "\n".join(market_data) if market_data else "Market data unavailable"
            
            enhanced_message = f"""
            {message}
            
            **CURRENT MARKET DATA (Real-time from Alpha Vantage):**
            {market_context}
            
            Please incorporate this real-time market data into your analysis and provide:
            - How current prices affect the valuation
            - Market trends and implications
            - Price assumptions to use
            - Risk factors based on current market
            """
            
            return self.send_message(enhanced_message)
            
        except Exception as e:
            print(f"Alpha Vantage integration error: {e}")
            return self.send_message(message)
    
    def analyze_comparable_companies(self, symbols: List[str]) -> str:
        """
        Analyze comparable oil & gas companies.
        
        Args:
            symbols: List of stock symbols (e.g., ['XOM', 'CVX', 'COP'])
        
        Returns:
            Comprehensive comparable company analysis
        """
        if not self.alpha_vantage:
            return "Alpha Vantage integration not available. Please configure API key."
        
        try:
            companies_data = []
            
            for symbol in symbols[:5]:  # Limit to 5 companies
                try:
                    analysis = self.alpha_vantage.analyze_oil_gas_company(symbol)
                    if 'error' not in analysis:
                        companies_data.append(analysis)
                except Exception as e:
                    print(f"Error analyzing {symbol}: {e}")
            
            if not companies_data:
                return "Unable to retrieve company data. Please check symbols."
            
            # Create comprehensive prompt
            companies_summary = []
            for comp in companies_data:
                info = comp.get('company_info', {})
                quote = comp.get('current_quote', {})
                val = comp.get('valuation', {})
                prof = comp.get('profitability', {})
                
                companies_summary.append(f"""
**{info.get('symbol')} - {info.get('name')}**
- Current Price: ${quote.get('price', 0):.2f}
- Market Cap: ${info.get('market_cap', 0)/1e9:.2f}B
- P/E Ratio: {val.get('pe_ratio', 0):.2f}
- Profit Margin: {prof.get('profit_margin', 0)*100:.1f}%
- ROE: {prof.get('roe', 0)*100:.1f}%
- Dividend Yield: {info.get('dividend_yield', 0)*100:.2f}%
                """)
            
            prompt = f"""
            Analyze these comparable oil & gas companies for M&A valuation purposes:
            
            {chr(10).join(companies_summary)}
            
            Provide a COMPREHENSIVE analysis including:
            
            ## 1. VALUATION MULTIPLES
            - Average P/E ratio and range
            - EV/EBITDA implications
            - Price/Book ratios
            - Recommended multiples for target valuation
            
            ## 2. PROFITABILITY BENCHMARKS
            - Profit margin comparison
            - ROE and ROA analysis
            - Operating efficiency metrics
            - Industry standards
            
            ## 3. MARKET POSITIONING
            - Market cap distribution
            - Competitive positioning
            - Growth prospects
            - Market share considerations
            
            ## 4. VALUATION IMPLICATIONS
            - What these comps suggest for target valuation
            - Appropriate discount/premium factors
            - Key value drivers
            - Risk adjustments needed
            
            ## 5. DEAL STRUCTURE INSIGHTS
            - Typical acquisition premiums (20-40%)
            - Payment structure trends
            - Synergy expectations
            - Integration considerations
            
            Make your analysis DETAILED, QUANTITATIVE, and ACTIONABLE for M&A decision-making.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error in comparable company analysis: {str(e)}"
    
    def get_market_intelligence(self) -> str:
        """
        Get comprehensive market intelligence for M&A context.
        
        Returns:
            Market intelligence report
        """
        if not self.alpha_vantage:
            return "Alpha Vantage integration not available."
        
        try:
            market_context = self.alpha_vantage.get_market_context()
            
            if 'error' in market_context:
                return f"Error retrieving market data: {market_context['error']}"
            
            commodities = market_context.get('commodities', {})
            economics = market_context.get('economic_indicators', {})
            
            prompt = f"""
            Provide a COMPREHENSIVE market intelligence briefing for oil & gas M&A:
            
            **COMMODITY PRICES (Current):**
            - WTI Crude Oil: ${commodities.get('wti_oil', {}).get('current', 0):.2f}/bbl
            - 12-Month Average: ${commodities.get('wti_oil', {}).get('avg_12m', 0):.2f}/bbl
            - Trend: {commodities.get('wti_oil', {}).get('trend', 'N/A')}
            - Brent Crude: ${commodities.get('brent_oil', {}).get('current', 0):.2f}/bbl
            - Natural Gas: ${commodities.get('natural_gas', {}).get('current', 0):.2f}/MMBtu
            
            **ECONOMIC INDICATORS:**
            - GDP Growth: {economics.get('gdp_growth', 0):.2f}%
            - Inflation Rate: {economics.get('inflation_rate', 0):.2f}%
            - Unemployment: {economics.get('unemployment_rate', 0):.2f}%
            - Fed Funds Rate: {economics.get('fed_funds_rate', 0):.2f}%
            
            Provide analysis covering:
            
            ## 1. MARKET ENVIRONMENT ASSESSMENT
            - Overall market conditions (bullish/bearish/neutral)
            - Commodity price trends and outlook
            - Economic cycle positioning
            - M&A market implications
            
            ## 2. VALUATION IMPLICATIONS
            - How current prices affect asset values
            - Discount rate considerations given Fed rate
            - Price assumptions to use in models
            - Risk premium adjustments
            
            ## 3. DEAL TIMING CONSIDERATIONS
            - Is now a good time to acquire? (buyer's/seller's market)
            - Price cycle positioning
            - Financing environment
            - Strategic timing recommendations
            
            ## 4. RISK FACTORS
            - Commodity price volatility
            - Economic headwinds/tailwinds
            - Regulatory environment
            - Market sentiment
            
            ## 5. STRATEGIC RECOMMENDATIONS
            - Deal structure suggestions
            - Hedging strategies
            - Contingency planning
            - Value protection mechanisms
            
            Make your analysis CURRENT, SPECIFIC, and ACTIONABLE for M&A decision-makers.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating market intelligence: {str(e)}"
    
    def analyze_anything(self, content: str, content_type: str = "auto") -> str:
        """
        Advanced AI that can read and analyze ANYTHING.
        
        Args:
            content: Any content (text, data, numbers, descriptions)
            content_type: Type hint ('financial', 'technical', 'legal', 'auto')
        
        Returns:
            Comprehensive analysis of the content
        """
        prompt = f"""
        As an expert analyst with deep knowledge across finance, engineering, legal, and business domains,
        provide a COMPREHENSIVE analysis of the following content:
        
        **CONTENT TO ANALYZE:**
        {content}
        
        **CONTENT TYPE:** {content_type}
        
        Provide a DETAILED analysis with these sections:
        
        ## 1. CONTENT IDENTIFICATION
        - What type of content is this?
        - What is its purpose?
        - What domain does it belong to?
        
        ## 2. KEY INFORMATION EXTRACTION
        - Main points and findings
        - Critical numbers and metrics
        - Important dates and timelines
        - Key entities mentioned
        
        ## 3. ANALYSIS & INSIGHTS
        - What does this tell us?
        - Patterns and trends identified
        - Strengths and weaknesses
        - Opportunities and risks
        
        ## 4. IMPLICATIONS
        - Business implications
        - Financial implications
        - Strategic implications
        - Operational implications
        
        ## 5. RED FLAGS & CONCERNS
        - Issues identified
        - Risks and concerns
        - Missing information
        - Inconsistencies
        
        ## 6. RECOMMENDATIONS
        - What actions to take
        - What to investigate further
        - What to verify
        - Next steps
        
        ## 7. SUMMARY
        - Executive summary (3-5 sentences)
        - Bottom line assessment
        - Key takeaways
        
        Make your analysis COMPREHENSIVE (500-1000 words), INSIGHTFUL, and ACTIONABLE.
        Use **bold** for key points and bullet points for clarity.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    # ==================== WEB SCRAPING INTEGRATION ====================
    
    def scrape_and_analyze_url(self, url: str, analysis_focus: str = "general") -> str:
        """
        Scrape a URL and provide AI analysis of the content.
        
        Args:
            url: URL to scrape and analyze
            analysis_focus: Focus area (general, company, financial, news, technical)
        
        Returns:
            Comprehensive AI analysis of scraped content
        """
        if not self.web_scraper:
            return "Web scraping not available. Please check configuration."
        
        try:
            # Scrape the URL
            scraped_data = self.web_scraper.scrape_url(url, extract_links=True)
            
            if not scraped_data['success']:
                return f"Failed to scrape URL: {scraped_data.get('error', 'Unknown error')}"
            
            # Create comprehensive prompt for AI analysis
            prompt = f"""
            Analyze this web content scraped from: {url}
            
            **PAGE INFORMATION:**
            - Title: {scraped_data.get('title', 'N/A')}
            - Meta Description: {scraped_data.get('meta_description', 'N/A')}
            - Content Length: {scraped_data.get('content_length', 0):,} characters
            - Number of Headings: {len(scraped_data.get('headings', []))}
            - Number of Links: {len(scraped_data.get('links', []))}
            - Number of Tables: {len(scraped_data.get('tables', []))}
            
            **MAIN HEADINGS:**
            {chr(10).join([f"- {h['text']}" for h in scraped_data.get('headings', [])[:10]])}
            
            **CONTENT PREVIEW (First 2000 characters):**
            {scraped_data.get('content', '')[:2000]}
            
            **ANALYSIS FOCUS:** {analysis_focus}
            
            Provide a COMPREHENSIVE analysis with these sections:
            
            ## 1. CONTENT SUMMARY
            - What is this webpage about?
            - Main topic and purpose
            - Target audience
            - Content type (article, company page, financial report, etc.)
            
            ## 2. KEY INFORMATION EXTRACTED
            - Main points and findings
            - Important facts and figures
            - Key entities mentioned (companies, people, locations)
            - Dates and timelines
            
            ## 3. DETAILED ANALYSIS
            - Content quality and credibility
            - Depth of information
            - Unique insights or data
            - Relevance to oil & gas M&A (if applicable)
            
            ## 4. BUSINESS IMPLICATIONS
            - How this information is useful
            - Strategic insights
            - Market implications
            - Competitive intelligence
            
            ## 5. DATA & METRICS
            - Numbers and statistics found
            - Financial data (if any)
            - Performance metrics
            - Trends identified
            
            ## 6. CREDIBILITY ASSESSMENT
            - Source reliability
            - Information freshness
            - Potential biases
            - Verification needed
            
            ## 7. ACTIONABLE INSIGHTS
            - What to do with this information
            - Follow-up actions
            - Additional research needed
            - Key takeaways
            
            ## 8. RELATED TOPICS
            - Connected subjects to explore
            - Suggested follow-up searches
            - Related companies or entities
            
            Make your analysis DETAILED (500-1000 words), INSIGHTFUL, and ACTIONABLE.
            Use **bold** for key points and bullet points for clarity.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error in web scraping analysis: {str(e)}"
    
    def scrape_multiple_urls_and_compare(self, urls: List[str]) -> str:
        """
        Scrape multiple URLs and provide comparative analysis.
        
        Args:
            urls: List of URLs to scrape and compare
        
        Returns:
            Comparative analysis of all URLs
        """
        if not self.web_scraper:
            return "Web scraping not available."
        
        try:
            # Scrape all URLs
            results = self.web_scraper.scrape_multiple_urls(urls[:5])  # Limit to 5 URLs
            
            # Prepare summary for each URL
            summaries = []
            for i, result in enumerate(results, 1):
                if result['success']:
                    summaries.append(f"""
**Source {i}: {result['url']}**
- Title: {result.get('title', 'N/A')}
- Content Length: {result.get('content_length', 0):,} characters
- Key Headings: {', '.join([h['text'] for h in result.get('headings', [])[:3]])}
- Content Preview: {result.get('content', '')[:300]}...
                    """)
                else:
                    summaries.append(f"""
**Source {i}: {result['url']}**
- Status: Failed to scrape
- Error: {result.get('error', 'Unknown')}
                    """)
            
            prompt = f"""
            Compare and analyze these {len(urls)} web sources:
            
            {chr(10).join(summaries)}
            
            Provide a COMPREHENSIVE comparative analysis:
            
            ## 1. OVERVIEW
            - Summary of each source
            - Main topics covered
            - Content types
            
            ## 2. KEY FINDINGS COMPARISON
            - Common themes across sources
            - Unique information in each source
            - Contradictions or disagreements
            - Consensus points
            
            ## 3. CREDIBILITY & RELIABILITY
            - Most reliable source
            - Potential biases in each
            - Information quality comparison
            
            ## 4. COMPREHENSIVE INSIGHTS
            - Combined intelligence from all sources
            - Holistic view of the topic
            - Market implications
            - Strategic insights
            
            ## 5. RECOMMENDATIONS
            - Which sources to prioritize
            - Additional sources needed
            - How to use this information
            - Next steps
            
            Make your analysis DETAILED and COMPARATIVE.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error in multi-URL analysis: {str(e)}"
    
    def research_topic(self, topic: str, num_sources: int = 5) -> str:
        """
        Research a topic by searching and analyzing multiple sources.
        
        Args:
            topic: Topic to research
            num_sources: Number of sources to analyze
        
        Returns:
            Comprehensive research report
        """
        if not self.web_scraper:
            return "Web scraping not available."
        
        try:
            # Search for the topic
            search_results = self.web_scraper.search_google(topic, num_sources)
            
            if not search_results or 'error' in search_results[0]:
                return f"Unable to search for topic: {topic}"
            
            # Scrape top results
            urls = [result['url'] for result in search_results if 'url' in result]
            scraped_results = self.web_scraper.scrape_multiple_urls(urls[:num_sources])
            
            # Prepare research data
            research_data = []
            for i, (search_result, scraped) in enumerate(zip(search_results, scraped_results), 1):
                if scraped['success']:
                    research_data.append(f"""
**Source {i}: {search_result.get('title', 'N/A')}**
- URL: {scraped['url']}
- Snippet: {search_result.get('snippet', 'N/A')}
- Content: {scraped.get('content', '')[:500]}...
                    """)
            
            prompt = f"""
            Research Report on: "{topic}"
            
            Based on analysis of {len(research_data)} sources:
            
            {chr(10).join(research_data)}
            
            Provide a COMPREHENSIVE research report:
            
            ## EXECUTIVE SUMMARY
            - Overview of findings
            - Key conclusions
            - Main insights
            
            ## DETAILED FINDINGS
            - What we learned about {topic}
            - Important facts and data
            - Expert opinions
            - Market trends
            
            ## ANALYSIS
            - Implications for oil & gas M&A
            - Strategic considerations
            - Risk factors
            - Opportunities
            
            ## DATA & METRICS
            - Quantitative findings
            - Statistics and numbers
            - Performance indicators
            
            ## RECOMMENDATIONS
            - How to use this information
            - Action items
            - Further research needed
            
            ## SOURCES QUALITY
            - Most valuable sources
            - Information gaps
            - Credibility assessment
            
            Make this a PROFESSIONAL research report (800-1200 words).
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error in topic research: {str(e)}"
    
    def analyze_company_website(self, url: str) -> str:
        """
        Analyze a company website for M&A intelligence.
        
        Args:
            url: Company website URL
        
        Returns:
            Company analysis based on website
        """
        if not self.web_scraper:
            return "Web scraping not available."
        
        try:
            # Scrape company website
            company_data = self.web_scraper.extract_company_info(url)
            
            if not company_data.get('title'):
                return f"Failed to analyze company website: {url}"
            
            prompt = f"""
            Analyze this company website for M&A intelligence:
            
            **COMPANY WEBSITE:** {url}
            
            **WEBSITE INFORMATION:**
            - Title: {company_data.get('title', 'N/A')}
            - Description: {company_data.get('description', 'N/A')}
            - Has About Page: {company_data.get('has_about_page', False)}
            - Has Contact Page: {company_data.get('has_contact_page', False)}
            - Has Investor Page: {company_data.get('has_investor_page', False)}
            - Oil & Gas Related: {company_data.get('mentions_oil', False) or company_data.get('mentions_gas', False)}
            - Energy Sector: {company_data.get('mentions_energy', False)}
            - Production Focus: {company_data.get('mentions_production', False)}
            - Reserves Mentioned: {company_data.get('mentions_reserves', False)}
            
            **CONTENT PREVIEW:**
            {company_data.get('content_preview', 'N/A')}
            
            Provide a COMPREHENSIVE company analysis:
            
            ## 1. COMPANY OVERVIEW
            - What does this company do?
            - Industry and sector
            - Business model
            - Geographic focus
            
            ## 2. M&A INTELLIGENCE
            - Potential acquisition target?
            - Company size indicators
            - Growth stage
            - Strategic value
            
            ## 3. BUSINESS ASSESSMENT
            - Core competencies
            - Market positioning
            - Competitive advantages
            - Technology and capabilities
            
            ## 4. FINANCIAL INDICATORS
            - Signs of financial health
            - Investment activity
            - Growth indicators
            - Profitability signals
            
            ## 5. STRATEGIC FIT
            - Synergy potential
            - Integration considerations
            - Cultural fit indicators
            - Geographic alignment
            
            ## 6. DUE DILIGENCE PRIORITIES
            - What to investigate further
            - Red flags to watch for
            - Key questions to ask
            - Information gaps
            
            ## 7. VALUATION CONSIDERATIONS
            - Value drivers identified
            - Risk factors
            - Growth potential
            - Market position
            
            ## 8. NEXT STEPS
            - Additional research needed
            - Who to contact
            - Information to request
            - Timeline considerations
            
            Make your analysis DETAILED and M&A-FOCUSED.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error analyzing company website: {str(e)}"


# Global instance (will be initialized with API key from environment)
gemini_service = None

def get_gemini_service(api_key: str, alpha_vantage_key: Optional[str] = None) -> GeminiService:
    """Get or create Gemini service instance with optional Alpha Vantage."""
    global gemini_service
    if gemini_service is None:
        gemini_service = GeminiService(api_key, alpha_vantage_key)
    return gemini_service

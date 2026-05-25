"""
Web Scraping Service for gathering information from websites.
Supports multiple scraping methods and intelligent content extraction.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
import re
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime
import time


class WebScraperService:
    """Service for web scraping and content extraction."""
    
    def __init__(self):
        """Initialize web scraper service."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def scrape_url(self, url: str, extract_links: bool = True, 
                   extract_images: bool = False) -> Dict:
        """
        Scrape content from a URL.
        
        Args:
            url: URL to scrape
            extract_links: Extract all links from page
            extract_images: Extract all images from page
        
        Returns:
            Scraped content and metadata
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract title
            title = soup.title.string if soup.title else ""
            
            # Extract meta description
            meta_desc = ""
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag:
                meta_desc = meta_tag.get("content", "")
            
            # Extract main content
            main_content = ""
            
            # Try to find main content area
            main_tags = soup.find_all(['article', 'main', 'div'], class_=re.compile(r'content|article|main|post'))
            if main_tags:
                main_content = ' '.join([tag.get_text(separator=' ', strip=True) for tag in main_tags])
            else:
                # Fallback to body
                body = soup.find('body')
                if body:
                    main_content = body.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            main_content = re.sub(r'\s+', ' ', main_content).strip()
            
            # Extract headings
            headings = []
            for i in range(1, 7):
                for heading in soup.find_all(f'h{i}'):
                    headings.append({
                        'level': i,
                        'text': heading.get_text(strip=True)
                    })
            
            # Extract paragraphs
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
            
            # Extract links
            links = []
            if extract_links:
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    links.append({
                        'text': link.get_text(strip=True),
                        'url': absolute_url
                    })
            
            # Extract images
            images = []
            if extract_images:
                for img in soup.find_all('img', src=True):
                    src = img['src']
                    absolute_url = urljoin(url, src)
                    images.append({
                        'alt': img.get('alt', ''),
                        'url': absolute_url
                    })
            
            # Extract tables
            tables = []
            for table in soup.find_all('table'):
                table_data = []
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    table_data.append([col.get_text(strip=True) for col in cols])
                if table_data:
                    tables.append(table_data)
            
            return {
                'success': True,
                'url': url,
                'title': title,
                'meta_description': meta_desc,
                'content': main_content,
                'content_length': len(main_content),
                'headings': headings,
                'paragraphs': paragraphs[:10],  # First 10 paragraphs
                'links': links[:50] if extract_links else [],  # First 50 links
                'images': images[:20] if extract_images else [],  # First 20 images
                'tables': tables,
                'scraped_at': datetime.now().isoformat(),
                'status_code': response.status_code
            }
        
        except requests.RequestException as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'error_type': type(e).__name__
            }
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'error_type': 'ParsingError'
            }
    
    def scrape_multiple_urls(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        """
        Scrape multiple URLs with delay between requests.
        
        Args:
            urls: List of URLs to scrape
            delay: Delay in seconds between requests
        
        Returns:
            List of scraped results
        """
        results = []
        for url in urls:
            result = self.scrape_url(url)
            results.append(result)
            if len(urls) > 1:
                time.sleep(delay)  # Be polite to servers
        return results
    
    def extract_company_info(self, url: str) -> Dict:
        """
        Extract company information from a website.
        
        Args:
            url: Company website URL
        
        Returns:
            Extracted company information
        """
        result = self.scrape_url(url, extract_links=True)
        
        if not result['success']:
            return result
        
        content = result['content'].lower()
        
        # Extract potential company info
        company_info = {
            'url': url,
            'title': result['title'],
            'description': result['meta_description'],
            'has_about_page': any('about' in link['url'].lower() for link in result['links']),
            'has_contact_page': any('contact' in link['url'].lower() for link in result['links']),
            'has_investor_page': any('investor' in link['url'].lower() for link in result['links']),
            'mentions_oil': 'oil' in content or 'petroleum' in content,
            'mentions_gas': 'gas' in content or 'natural gas' in content,
            'mentions_energy': 'energy' in content,
            'mentions_production': 'production' in content,
            'mentions_reserves': 'reserves' in content or 'reservoir' in content,
            'content_preview': result['content'][:500]
        }
        
        return company_info
    
    def search_google(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search Google and return results (simplified version).
        Note: For production, use Google Custom Search API.
        
        Args:
            query: Search query
            num_results: Number of results to return
        
        Returns:
            List of search results
        """
        # This is a simplified version
        # For production, integrate with Google Custom Search API
        search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
        
        try:
            response = self.session.get(search_url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for g in soup.find_all('div', class_='g')[:num_results]:
                title_elem = g.find('h3')
                link_elem = g.find('a')
                snippet_elem = g.find('div', class_=['VwiC3b', 'yXK7lf'])
                
                if title_elem and link_elem:
                    results.append({
                        'title': title_elem.get_text(),
                        'url': link_elem.get('href', ''),
                        'snippet': snippet_elem.get_text() if snippet_elem else ''
                    })
            
            return results
        except Exception as e:
            return [{'error': str(e)}]
    
    def extract_news_articles(self, url: str) -> Dict:
        """
        Extract news article content.
        
        Args:
            url: News article URL
        
        Returns:
            Extracted article information
        """
        result = self.scrape_url(url)
        
        if not result['success']:
            return result
        
        soup = BeautifulSoup(result['content'], 'html.parser')
        
        # Try to extract article metadata
        article_info = {
            'url': url,
            'title': result['title'],
            'content': result['content'],
            'paragraphs': result['paragraphs'],
            'headings': result['headings'],
            'word_count': len(result['content'].split()),
            'scraped_at': result['scraped_at']
        }
        
        return article_info
    
    def extract_financial_data(self, url: str) -> Dict:
        """
        Extract financial data from a webpage.
        
        Args:
            url: URL containing financial data
        
        Returns:
            Extracted financial information
        """
        result = self.scrape_url(url)
        
        if not result['success']:
            return result
        
        content = result['content']
        
        # Extract numbers that look like financial data
        # Pattern for currency amounts
        currency_pattern = r'\$\s*[\d,]+\.?\d*[MBK]?'
        amounts = re.findall(currency_pattern, content)
        
        # Pattern for percentages
        percentage_pattern = r'\d+\.?\d*\s*%'
        percentages = re.findall(percentage_pattern, content)
        
        # Extract tables (often contain financial data)
        tables = result.get('tables', [])
        
        return {
            'success': True,
            'url': url,
            'currency_amounts': amounts[:20],  # First 20 amounts
            'percentages': percentages[:20],  # First 20 percentages
            'tables': tables,
            'content_preview': content[:1000]
        }
    
    def scrape_with_analysis(self, url: str, analysis_type: str = "general") -> Dict:
        """
        Scrape URL and prepare for AI analysis.
        
        Args:
            url: URL to scrape
            analysis_type: Type of analysis (general, company, financial, news)
        
        Returns:
            Scraped content formatted for AI analysis
        """
        if analysis_type == "company":
            return self.extract_company_info(url)
        elif analysis_type == "financial":
            return self.extract_financial_data(url)
        elif analysis_type == "news":
            return self.extract_news_articles(url)
        else:
            return self.scrape_url(url, extract_links=True, extract_images=False)
    
    def extract_structured_data(self, url: str) -> Dict:
        """
        Extract structured data (JSON-LD, microdata) from webpage.
        
        Args:
            url: URL to scrape
        
        Returns:
            Extracted structured data
        """
        try:
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            structured_data = []
            
            # Extract JSON-LD
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    structured_data.append({
                        'type': 'json-ld',
                        'data': data
                    })
                except:
                    pass
            
            # Extract Open Graph tags
            og_data = {}
            for meta in soup.find_all('meta', property=re.compile(r'^og:')):
                property_name = meta.get('property', '')
                content = meta.get('content', '')
                og_data[property_name] = content
            
            if og_data:
                structured_data.append({
                    'type': 'open-graph',
                    'data': og_data
                })
            
            # Extract Twitter Card tags
            twitter_data = {}
            for meta in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')}):
                name = meta.get('name', '')
                content = meta.get('content', '')
                twitter_data[name] = content
            
            if twitter_data:
                structured_data.append({
                    'type': 'twitter-card',
                    'data': twitter_data
                })
            
            return {
                'success': True,
                'url': url,
                'structured_data': structured_data
            }
        
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }
    
    def get_page_metadata(self, url: str) -> Dict:
        """
        Get comprehensive page metadata.
        
        Args:
            url: URL to analyze
        
        Returns:
            Page metadata
        """
        try:
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            metadata = {
                'url': url,
                'title': soup.title.string if soup.title else "",
                'meta_tags': {},
                'links_count': len(soup.find_all('a')),
                'images_count': len(soup.find_all('img')),
                'headings_count': {
                    f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)
                },
                'has_forms': len(soup.find_all('form')) > 0,
                'has_tables': len(soup.find_all('table')) > 0,
                'content_length': len(soup.get_text()),
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'server': response.headers.get('server', ''),
                'last_modified': response.headers.get('last-modified', '')
            }
            
            # Extract all meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
                content = meta.get('content')
                if name and content:
                    metadata['meta_tags'][name] = content
            
            return metadata
        
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }


# Global instance
web_scraper_service = None

def get_web_scraper_service() -> WebScraperService:
    """Get or create web scraper service instance."""
    global web_scraper_service
    if web_scraper_service is None:
        web_scraper_service = WebScraperService()
    return web_scraper_service

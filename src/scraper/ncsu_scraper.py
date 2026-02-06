"""NCSU Website Scraper"""
import os
import requests
import time
from typing import List
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin
import logging

# Conditional Selenium import (may not be available in all environments)
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

from .models import ScrapingConfig, SearchResult, ScrapedPage

class NCSUScraper:
    """Scraper for NCSU website"""
    
    def __init__(self, config: ScrapingConfig = None):
        self.config = config or ScrapingConfig()
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://www.ncsu.edu"
        self.search_url = "https://www.ncsu.edu/search/"
        
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search NCSU website"""
        self.logger.info(f"Searching for: {query}")
        results = []
        
        # Check if running on Hugging Face Spaces or other restricted environments
        is_hf_space = os.getenv('SPACE_ID') is not None or os.getenv('HF_SPACE') is not None
        is_restricted = os.getenv('DISABLE_SELENIUM', '').lower() == 'true'
        
        # Skip Selenium if in restricted environment, disabled, or not available
        if (is_hf_space or is_restricted or not SELENIUM_AVAILABLE) and self.config.selenium_enabled:
            self.logger.warning("Selenium not available in this environment, using fallback search method")
            return self._search_without_selenium(query, max_results)
        
        # If Selenium is disabled in config, use fallback
        if not self.config.selenium_enabled:
            return self._search_without_selenium(query, max_results)
        
        try:
            # Use Selenium for JavaScript-rendered search
            chrome_options = Options()
            
            # 🔧 Anti-detection options to bypass reCAPTCHA
            # chrome_options.add_argument('--headless')  # 旧版headless容易被检测
            chrome_options.add_argument('--headless=new')  # 使用新版headless模式，更难检测
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # 🛡️ 反自动化检测
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(options=chrome_options)
            
            # 🎭 隐藏webdriver特征
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en']
                    });
                '''
            })
            
            try:
                search_query_url = f"{self.search_url}?q={quote_plus(query)}"
                driver.get(search_query_url)
                
                # Wait for results to load (增加等待时间，让页面完全加载)
                time.sleep(5)  # 从3秒增加到5秒
                
                # Get page source and parse
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # Find search results
                search_results = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and ('result' in x.lower() or 'search' in x.lower()))
                
                if not search_results:
                    # Try alternative selectors
                    search_results = soup.find_all('a', href=True)
                
                for result in search_results[:max_results * 3]:  # Get more than needed
                    try:
                        # Try to find title and link
                        if result.name == 'a':
                            link = result
                            title = result.get_text(strip=True)
                        else:
                            link = result.find('a', href=True)
                            title_elem = result.find(['h2', 'h3', 'h4', 'a'])
                            title = title_elem.get_text(strip=True) if title_elem else ""
                        
                        if not link or not title:
                            continue
                            
                        url = link.get('href', '')
                        
                        # Filter for NCSU URLs
                        if not url.startswith('http'):
                            url = urljoin(self.base_url, url)
                        
                        if 'ncsu.edu' not in url:
                            continue
                        
                        # Get snippet
                        snippet_elem = result.find(['p', 'div', 'span'], class_=lambda x: x and 'snippet' in x.lower() if x else False)
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                        
                        if len(title) > 5:  # Basic validation
                            results.append(SearchResult(
                                title=title[:200],
                                url=url,
                                snippet=snippet[:500]
                            ))
                        
                        if len(results) >= max_results:
                            break
                            
                    except Exception as e:
                        self.logger.debug(f"Error parsing result: {e}")
                        continue
                        
            finally:
                driver.quit()
                
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            
        return results[:max_results]
    
    def scrape_pages(self, search_results: List[SearchResult]) -> List[ScrapedPage]:
        """Scrape content from search results"""
        scraped_pages = []
        
        for i, result in enumerate(search_results):
            self.logger.info(f"Scraping {i+1}/{len(search_results)}: {result.url}")
            
            try:
                # Add delay between requests
                if i > 0:
                    time.sleep(self.config.delay)
                
                # Use requests to get content
                headers = {'User-Agent': self.config.user_agent}
                response = requests.get(result.url, headers=headers, timeout=self.config.timeout)
                response.raise_for_status()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                    script.decompose()
                
                # Get text content
                text = soup.get_text(separator=' ', strip=True)
                
                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                scraped_pages.append(ScrapedPage(
                    title=result.title,
                    url=result.url,
                    content=text,
                    extraction_success=True
                ))
                
                self.logger.info(f"  ✓ Extracted {len(text)} characters")
                
            except Exception as e:
                self.logger.error(f"  ✗ Error scraping {result.url}: {e}")
                scraped_pages.append(ScrapedPage(
                    title=result.title,
                    url=result.url,
                    content="",
                    extraction_success=False
                ))
        
        return scraped_pages
    
    def _search_without_selenium(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """
        Fallback search method that doesn't require Selenium.
        Uses direct HTTP requests to search NCSU website.
        """
        self.logger.info(f"Using fallback search method (no Selenium) for: {query}")
        results = []
        
        try:
            # Try to use NCSU search API or direct search URL
            search_query_url = f"{self.search_url}?q={quote_plus(query)}"
            
            headers = {
                'User-Agent': self.config.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = requests.get(search_query_url, headers=headers, timeout=self.config.timeout)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find search results (various possible selectors)
            search_results = []
            
            # Try Google Custom Search result selectors
            search_results = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and (
                'result' in x.lower() or 
                'search' in x.lower() or
                'gs-webResult' in x.lower() or
                'gsc-webResult' in x.lower()
            ))
            
            # If no results found, try finding all links
            if not search_results:
                search_results = soup.find_all('a', href=True)
            
            for result in search_results[:max_results * 3]:
                try:
                    # Extract title and URL
                    if result.name == 'a':
                        link = result
                        title = result.get_text(strip=True)
                    else:
                        link = result.find('a', href=True)
                        title_elem = result.find(['h2', 'h3', 'h4', 'a', 'span'])
                        title = title_elem.get_text(strip=True) if title_elem else ""
                    
                    if not link or not title:
                        continue
                    
                    url = link.get('href', '')
                    
                    # Filter for NCSU URLs
                    if not url.startswith('http'):
                        url = urljoin(self.base_url, url)
                    
                    if 'ncsu.edu' not in url:
                        continue
                    
                    # Get snippet
                    snippet_elem = result.find(['p', 'div', 'span'], class_=lambda x: x and 'snippet' in x.lower() if x else False)
                    if not snippet_elem:
                        snippet_elem = result.find('p')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    if len(title) > 5:  # Basic validation
                        results.append(SearchResult(
                            title=title[:200],
                            url=url,
                            snippet=snippet[:500]
                        ))
                    
                    if len(results) >= max_results:
                        break
                        
                except Exception as e:
                    self.logger.debug(f"Error parsing result: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"Fallback search error: {e}")
            # Return empty results if search fails
            pass
        
        return results[:max_results]



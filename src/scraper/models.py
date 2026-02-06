"""Data models for scraper"""
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

@dataclass
class ScrapingConfig:
    """Configuration for web scraping"""
    selenium_enabled: bool = True
    enhanced_extraction: bool = True
    timeout: int = 30
    user_agent: str = "NCSU Research Assistant Bot 1.0"
    delay: float = 1.0
    max_retries: int = 3

@dataclass
class SearchResult:
    """Search result data"""
    title: str
    url: str
    snippet: str = ""
    
@dataclass
class ScrapedPage:
    """Scraped page data"""
    title: str
    url: str
    content: str
    extraction_success: bool = True
    word_count: int = 0
    
    def __post_init__(self):
        if not self.word_count:
            self.word_count = len(self.content.split())


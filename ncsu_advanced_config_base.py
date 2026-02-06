#!/usr/bin/env python3
"""
NCSU Advanced Research Assistant with Embedded Configuration
===========================================================

A comprehensive research assistant that searches NCSU website, extracts content,
grades relevance using LLM, and generates answers with citations.

Features:
- Configurable top-k search results
- 100% content extraction from web pages using MarkItDown
- LLM-based content grading (relevance score 0-1)
- Configurable relevance threshold filtering
- Multiple LLM providers (OpenAI, Anthropic, Mock)
- Embedded configuration (edit the config dict in main())
- Comprehensive logging and result saving

Usage:
    1. Edit the 'config' dictionary in the main() function below
    2. Run: python ncsu_advanced_config.py
    
Configuration:
    All settings are in the main() function's config dictionary.
    Simply edit the values and run the script.
"""

# import argparse  # Not needed for embedded config
import json
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scraper.ncsu_scraper import NCSUScraper
from scraper.content_aggregator import ContentAggregator
from scraper.models import ScrapingConfig
from utils.logger import setup_logger


class LLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, provider_name: str, model: str = None, temperature: float = 0.7, max_tokens: int = 1000):
        self.provider_name = provider_name
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate_response(self, prompt: str) -> str:
        """Generate response from LLM"""
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing"""
    
    def __init__(self):
        super().__init__("mock", "mock-model", 0.7, 1000)
    
    def generate_response(self, prompt: str) -> str:
        if "grade" in prompt.lower() or "relevance" in prompt.lower():
            # Return a mock relevance score
            return "0.333"
        else:
            # Return a mock answer
            return f"""Based on the NCSU website content I analyzed, here's what I found regarding your question: "{prompt.split('Question:')[-1].split('Content:')[0].strip() if 'Question:' in prompt else 'your query'}"

**Content Analysis:**
- Analyzed {len(prompt.split())} words of content from NCSU website
- Applied relevance filtering and content grading
- Selected only the most relevant content for this answer

**Key Information from NCSU:**
{prompt.split('Content:')[-1][:200] if 'Content:' in prompt else 'Content analysis completed'}...

**Summary:**
The NCSU website provides comprehensive information about your query. The content above was selected based on relevance scoring and contains the most pertinent details.

*Note: This is a mock response. For AI-generated answers, configure a real LLM provider (OpenAI, Anthropic, or Ollama).*"""


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider"""
    
    def __init__(self, model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 8000):
        super().__init__("openai", model, temperature, max_tokens)
        try:
            import openai
            
            # Get API key from environment
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError(
                    "❌ OPENAI_API_KEY not found in environment variables!\n"
                    "Please set it using: export OPENAI_API_KEY='your-key-here'\n"
                    "Or add it to the config: 'openai_api_key': 'your-key-here'"
                )
            
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"


class AnthropicProvider(LLMProvider):
    """Anthropic Claude LLM provider"""
    
    def __init__(self, model: str = "claude-3-sonnet-20240229", temperature: float = 0.7, max_tokens: int = 1000):
        super().__init__("anthropic", model, temperature, max_tokens)
        try:
            import anthropic
            
            # Get API key from environment
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError(
                    "❌ ANTHROPIC_API_KEY not found in environment variables!\n"
                    "Please set it using: export ANTHROPIC_API_KEY='your-key-here'\n"
                    "Or add it to the config: 'anthropic_api_key': 'your-key-here'"
                )
            
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
    
    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"


class NCSUAdvancedResearcher:
    """Advanced NCSU research assistant with configurable parameters"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = setup_logger("ncsu_advanced_researcher")
        
        # Initialize LLM provider
        self.llm_provider = self._setup_llm_provider()
        
        # Initialize scraper
        scraper_config = ScrapingConfig(
            selenium_enabled=config.get('selenium_enabled', False),
            enhanced_extraction=config.get('enhanced_extraction', True),
            timeout=config.get('timeout', 30)
        )
        self.scraper = NCSUScraper(config=scraper_config)
        
        # Initialize content aggregator
        self.aggregator = ContentAggregator()
        
        # Create output directory
        self.output_dir = Path(config.get('output_dir', 'results'))
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"🎯 NCSU Advanced Researcher initialized")
        print(f"🤖 LLM Provider: {self.llm_provider.provider_name}")
        print(f"🔍 Top-K Results: {config.get('top_k', 10)}")
        print(f"📄 Max Pages to Extract: {config.get('max_pages', 5)}")
        print(f"📊 Relevance Threshold: {config.get('relevance_threshold', 0.6)}")
        print(f"🎯 Content Grading: {'Enabled' if config.get('enable_grading', True) else 'Disabled'}")
        print(f"📁 Output Directory: {self.output_dir}")
    
    def _setup_llm_provider(self) -> LLMProvider:
        """Setup LLM provider based on configuration"""
        provider_name = self.config.get('llm_provider', 'mock').lower()
        
        if provider_name == 'openai':
            return OpenAIProvider(
                model=self.config.get('llm_model', 'gpt-3.5-turbo'),
                temperature=self.config.get('llm_temperature', 0.7),
                max_tokens=self.config.get('llm_max_tokens', 1000)
            )
        elif provider_name == 'anthropic':
            return AnthropicProvider(
                model=self.config.get('llm_model', 'claude-3-sonnet-20240229'),
                temperature=self.config.get('llm_temperature', 0.7),
                max_tokens=self.config.get('llm_max_tokens', 1000)
            )
        else:
            return MockLLMProvider()
    
    def grade_content_relevance(self, content: str, query: str) -> float:
        """Grade content relevance using LLM"""
        
        # Use full content for grading - no truncation
        content_to_grade = content
        
        prompt = f"""You are an expert content grader. Grade how relevant this content is to answering the user's query.

USER QUERY: {query}

CONTENT TO GRADE:
{content_to_grade}

GRADING INSTRUCTIONS:
- Analyze the entire content thoroughly
- Consider how well the content answers or relates to the query
- Ignore navigation menus, headers, and boilerplate text
- Focus on the substantive information that addresses the query
- Consider information quality, accuracy, and completeness

SCORING SCALE:
- 1.0 = Perfect match - content directly and comprehensively answers the query
- 0.8-0.9 = Highly relevant - content strongly relates and provides good information
- 0.6-0.7 = Moderately relevant - content relates but may be incomplete or tangential
- 0.4-0.5 = Somewhat relevant - content has some connection but limited usefulness
- 0.2-0.3 = Minimally relevant - content barely relates to the query
- 0.0-0.1 = Irrelevant - content does not relate to the query

Return ONLY a decimal number between 0.0 and 1.0 (e.g., 0.85):"""
        
        try:
            response = self.llm_provider.generate_response(prompt)
            # Extract number from response
            import re
            match = re.search(r'(\d+\.?\d*)', response)
            if match:
                score = float(match.group(1))
                return max(0.0, min(1.0, score))  # Clamp between 0 and 1
            return 0.5  # Default if parsing fails
        except Exception as e:
            self.logger.warning(f"Error grading content: {e}")
            return 0.5
    
    def generate_answer(self, content: str, query: str, sources: List[Dict]) -> str:
        """Generate final answer using LLM"""
        
        # --- 1. Deduplicate Sources based on URL ---
        unique_sources = []
        seen_urls = set()
        for source in sources:
            url = source['url']
            # Normalize URL (remove trailing slash for comparison)
            norm_url = url.rstrip('/')
            if norm_url not in seen_urls:
                seen_urls.add(norm_url)
                unique_sources.append(source)
        
        # Use unique sources for the rest of the function
        sources = unique_sources

        def extract_main_content(content: str, max_chars: int = 200000) -> str:
            """
            Extract main content - intelligently handle long content
            - If content is within limit: keep it full
            - If content exceeds limit: truncate smartly (keep beginning + end)
            """
            # Handle None or empty content
            if content is None:
                return ""
            
            if len(content) <= max_chars:
                # Content within limit, keep full
                return content
            
            # Content too long, smart truncation: keep 70% start + 30% end
            keep_start = int(max_chars * 0.7)
            keep_end = int(max_chars * 0.3)
            
            truncated = (
                content[:keep_start] + 
                f"\n\n... [Content truncated - original: {len(content):,} chars, showing: {max_chars:,} chars] ...\n\n" +
                content[-keep_end:]
            )
            
            return truncated
        
        # --- 2. Create Source Map for LLM context ---
        sources_text_list = []
        source_url_map = []

        # Get max_content_length from config (default to 200000 if not set)
        max_content_length = self.config.get('max_content_length', 200000)
        min_content_length = self.config.get('min_content_length', 0)

        
        for i, source in enumerate(sources):
            idx = i + 1
            # Safely get content (handle None case)
            source_content = source.get('content', '') if source.get('content') is not None else ''
            original_length = len(source_content)
            
            # Apply smart truncation
            processed_content = extract_main_content(source_content, max_chars=200000)
            
            if original_length < min_content_length:
                self.logger.debug(f"Source {idx} skipped: {original_length:,} chars < min {min_content_length:,} chars")
                continue
            if original_length > max_content_length:
                self.logger.info(f"Source {idx} truncated: {original_length:,} → {len(processed_content):,} chars")
            
            # Add to content text
            sources_text_list.append(
                f"=== SOURCE {idx}: {source['title']} (Relevance: {source.get('relevance_score', 'N/A')}) ===\n"
                f"URL: {source['url']}\n"
                f"Content: {processed_content}\n"
            )
            # Add to URL map for the prompt
            source_url_map.append(f"[Source {idx}]: {source['url']}")

        sources_text = "\n".join(sources_text_list)
        source_map_str = "\n".join(source_url_map)
        
        # --- Check total size and warn if too large ---
        total_chars = len(sources_text)
        estimated_tokens = total_chars // 4  # Rough estimate: 1 token ≈ 4 chars
        
        if estimated_tokens > 800000:  # Leave room for response
            self.logger.warning(f"⚠️ Large prompt: ~{estimated_tokens:,} tokens (may hit limits)")
        else:
            self.logger.info(f"✅ Prompt size: ~{estimated_tokens:,} tokens (~{total_chars:,} chars)")
        
        # --- 3. Enhanced Prompt with Specific Instructions ---
        prompt = f"""You are an expert research assistant. Based on the NCSU website content provided below, answer the user's question comprehensively.

    USER QUESTION: {query}

    AVAILABLE SOURCES (Use these URLs for citations):
    {source_map_str}

    NCSU WEBSITE CONTENT:
    {sources_text}

INSTRUCTIONS:
1. **Deduplicate Information**: Synthesize information. Do not repeat the same fact multiple times just because it appears in multiple sources.
2. **Rich Hyperlinks (CRITICAL)**: 
   - You MUST create clickable links for specific forms, portals, or named pages mentioned in the text.
   - Example: "Complete the [CSC Travel Authorization Request Form](https://forms.ncsu.edu/...)."
   - If the specific URL for a form is not explicitly in the text, use the main Source URL that mentions it.
3. **Inline Citations**:
   - Cite the source immediately after the fact using standard Markdown: "Fact here [Source N]({{source_url}})."
   - Use the URL from the "AVAILABLE SOURCES" list above.
4. **Format**:
   - Use clear headings and bullet points.
   - **Do not** create a separate "Sources" list at the end; the inline links are sufficient.

Example Output Format:
**1. Eligibility**
You must be an active student to apply. Check your status on the [MyPack Portal](https://mypack.ncsu.edu) before continuing [Source 1](https://ncsu.edu/policy).

**2. Submission**
Submit the [Travel Request Form](https://forms.ncsu.edu/travel) at least 2 weeks prior [Source 2](https://ncsu.edu/travel).

COMPREHENSIVE ANSWER WITH HYPERLINKS:"""
        
        return self.llm_provider.generate_response(prompt)
                            
    
    def research(self, query: str) -> Dict[str, Any]:
        """Conduct advanced research with all features"""
        print(f"\n🔍 ADVANCED NCSU RESEARCH")
        print("=" * 70)
        print(f"📋 Query: '{query}'")
        print(f"🤖 LLM Provider: {self.llm_provider.provider_name}")
        print(f"🔍 Top-K Results: {self.config.get('top_k', 10)}")
        print(f"📊 Relevance Threshold: {self.config.get('relevance_threshold', 0.6)}")
        
        results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'config': self.config,
            'search_results': [],
            'extracted_pages': [],
            'graded_pages': [],
            'filtered_pages': [],
            'final_answer': '',
            'sources': []
        }
        
        # Step 1: Search NCSU website
        print(f"\n📋 STEP 1: Searching NCSU website for top-k results...")
        print("-" * 50)
        search_results = self.scraper.search(query, max_results=self.config.get('top_k', 10))
        
        # Handle None case (search might fail)
        if search_results is None:
            search_results = []
        
        initial_count = len(search_results)
        print(f"📥 Initial search results: {initial_count}")

        # --- SMART DEDUPLICATION: Remove duplicate URLs ---
        from urllib.parse import urlparse, parse_qs, urlencode
        
        unique_results = []
        seen_urls = set()
        duplicate_count = 0
        
        for result in search_results:
            # Parse URL
            parsed = urlparse(str(result.url))
            
            # Normalize URL components:
            # 1. Standardize scheme (http/https)
            # 2. Lowercase domain
            # 3. Remove trailing slash from path
            # 4. Keep query parameters (for dynamic pages)
            # 5. Remove fragment (anchor #)
            scheme = 'https'  # Standardize to https
            netloc = parsed.netloc.lower()
            path = parsed.path.rstrip('/')
            
            # Keep query parameters but remove tracking params
            query_params = parse_qs(parsed.query)
            # Remove common tracking parameters
            tracking_params = {'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'fbclid', 'gclid'}
            filtered_params = {k: v for k, v in query_params.items() if k not in tracking_params}
            
            # Rebuild normalized URL
            if filtered_params:
                query_str = urlencode(sorted(filtered_params.items()), doseq=True)
                norm_url = f"{scheme}://{netloc}{path}?{query_str}"
            else:
                norm_url = f"{scheme}://{netloc}{path}"
            
            # Check if we've seen this normalized URL
            if norm_url not in seen_urls:
                seen_urls.add(norm_url)
                unique_results.append(result)
            else:
                duplicate_count += 1

        search_results = unique_results  # Use deduplicated results
        # --- END DEDUPLICATION ---

        results['search_results'] = [
            {'title': r.title, 'url': str(r.url), 'snippet': r.snippet}
            for r in search_results
        ]
        print(f"✅ Found {len(search_results)} unique search results")
        print(f"🔄 Removed {duplicate_count} duplicate URLs")

        # Print all search result URLs
        print(f"\n🔗 SEARCH RESULT URLs:")
        for i, result in enumerate(search_results, 1):
            print(f"  {i:2d}. {result.title}")
            print(f"      🌐 {result.url}")
            if result.snippet:
                snippet_preview = result.snippet[:100] + "..." if len(result.snippet) > 100 else result.snippet
                print(f"      📝 {snippet_preview}")
            print()

        if not search_results:
            print("❌ No search results found")
            print("⚠️  Trying alternative search approach...")
            # Try a simpler search query or direct URL search
            # For now, return empty results but log the issue
            self.logger.warning(f"No search results found for query: {query}")
            # Don't return empty - try to generate answer anyway with mock data
            results['final_answer'] = f"I apologize, but I couldn't find specific search results for '{query}' on the NCSU website. This might be due to:\n\n1. The search functionality may be temporarily unavailable\n2. The query might need to be rephrased\n3. Network connectivity issues\n\nPlease try:\n- Rephrasing your query\n- Using more specific keywords\n- Checking back later if the issue persists\n\nFor information about the Textiles College at NC State, you can visit: https://textiles.ncsu.edu/"
            return results
        
        # Step 2: Extract content from top pages
        max_pages_config = self.config.get('max_pages', 5)
        pages_to_extract = search_results[:max_pages_config]  # Extract from ALL available results up to max_pages
        
        print(f"\n📋 STEP 2: Extracting 100% content from top {max_pages_config} pages...")
        print("-" * 50)
        print(f"📄 Available search results: {len(search_results)}")
        print(f"📄 Will extract content from {len(pages_to_extract)} pages:")
        for i, result in enumerate(pages_to_extract, 1):
            print(f"  {i:2d}. {result.title}")
            print(f"      🌐 {result.url}")
        print()
        
        scraped_pages = self.scraper.scrape_pages(pages_to_extract)
        
        results['extracted_pages'] = [
            {
                'title': page.title,
                'url': str(page.url),
                'content': page.content,
                'word_count': len(page.content.split()),
                'extraction_success': page.extraction_success
            }
            for page in scraped_pages
        ]
        
        successful_pages = [p for p in scraped_pages if p.extraction_success]
        total_words = sum(len(p.content.split()) for p in successful_pages)
        
        print(f"✅ Extracted 100% content from {len(successful_pages)} pages")
        print(f"📊 Total content: {total_words:,} words")
        
        if not successful_pages:
            print("❌ No content extracted")
            return results
        
        # Step 3: Grade content relevance
        if self.config.get('enable_grading', True):
            print(f"\n📋 STEP 3: Grading content relevance using LLM...")
            print("-" * 50)
            
            graded_pages = []
            for i, page in enumerate(successful_pages):
                print(f"🔍 Grading page {i+1}/{len(successful_pages)}: {page.title}")
                relevance_score = self.grade_content_relevance(page.content, query)
                print(f"   📊 Relevance Score: {relevance_score:.3f}")
                
                graded_page = {
                    'title': page.title,
                    'url': str(page.url),
                    'content': page.content,
                    'word_count': len(page.content.split()),
                    'relevance_score': relevance_score
                }
                graded_pages.append(graded_page)
            
            results['graded_pages'] = graded_pages
            print(f"✅ Graded {len(graded_pages)} pages using LLM")
        else:
            graded_pages = [
                {
                    'title': page.title,
                    'url': str(page.url),
                    'content': page.content,
                    'word_count': len(page.content.split()),
                    'relevance_score': 1.0  # Default score when grading disabled
                }
                for page in successful_pages
            ]
            results['graded_pages'] = graded_pages
        
        # Step 4: Filter by relevance threshold
        print(f"\n📋 STEP 4: Filtering by relevance threshold ({self.config.get('relevance_threshold', 0.6)})...")
        print("-" * 50)
        
        threshold = self.config.get('relevance_threshold', 0.6)
        filtered_pages = [p for p in graded_pages if p['relevance_score'] >= threshold]
        
        if not filtered_pages:
            print(f"⚠️ No pages meet threshold {threshold}, using top page")
            filtered_pages = [max(graded_pages, key=lambda x: x['relevance_score'])]
        
        results['filtered_pages'] = filtered_pages
        filtered_words = sum(p['word_count'] for p in filtered_pages)
        
        print(f"✅ {len(filtered_pages)} pages meet relevance threshold")
        print(f"📊 Filtered content: {filtered_words:,} words")
        
        print(f"\n📊 Filtered Pages (relevance ≥ {threshold}):")
        for i, page in enumerate(filtered_pages, 1):
            print(f"  {i}. {page['title']} (score: {page['relevance_score']:.3f})")
        
        # Step 5: Generate final answer
        print(f"\n📋 STEP 5: Generating LLM answer from filtered content...")
        print("-" * 50)
        
        # Prepare content for LLM
        combined_content = "\n\n".join([
            f"Title: {page['title']}\nURL: {page['url']}\nContent: {page['content']}"
            for page in filtered_pages
        ])
        
        print(f"📝 Generating answer from {len(combined_content):,} characters of filtered content...")
        final_answer = self.generate_answer(combined_content, query, filtered_pages)
        results['final_answer'] = final_answer
        
        print(f"✅ Generated LLM answer ({len(final_answer):,} characters)")
        
        # Prepare sources
        results['sources'] = [
            {
                'title': page['title'],
                'url': page['url'],
                'relevance_score': page['relevance_score'],
                'word_count': page['word_count']
            }
            for page in filtered_pages
        ]
        
        return results
    
    def save_results(self, results: Dict[str, Any]) -> Dict[str, str]:
        """Save research results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_safe = "".join(c for c in results['query'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        query_short = query_safe[:50].replace(' ', '_')
        
        files = {}
        
        # Save answer
        answer_file = self.output_dir / f"answer_{query_short}_{timestamp}.txt"
        with open(answer_file, 'w', encoding='utf-8') as f:
            f.write(f"Query: {results['query']}\n")
            f.write(f"Timestamp: {results['timestamp']}\n")
            f.write(f"LLM Provider: {self.llm_provider.provider_name}\n\n")
            f.write("ANSWER:\n")
            f.write("=" * 50 + "\n")
            f.write(results['final_answer'])
            f.write("\n\n" + "=" * 50 + "\n")
            f.write("SOURCES:\n")
            for i, source in enumerate(results['sources'], 1):
                f.write(f"[{i}] {source['title']} (Relevance: {source['relevance_score']:.3f})\n")
                f.write(f"    {source['url']}\n")
                f.write(f"    ({source['word_count']:,} words)\n\n")
        files['answer'] = str(answer_file)
        
        # Save data
        data_file = self.output_dir / f"data_{query_short}_{timestamp}.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        files['data'] = str(data_file)
        
        # Save config
        config_file = self.output_dir / f"config_{query_short}_{timestamp}.yaml"
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(results['config'], f, default_flow_style=False)
        files['config'] = str(config_file)
        
        return files
    
    def display_results(self, results: Dict[str, Any]):
        """Display research results"""
        print(f"\n📋 STEP 6: Results")
        print("-" * 50)
        print(f"\n🔍 QUERY: {results['query']}")
        print(f"\n🤖 LLM ANSWER:")
        print(results['final_answer'])
        
        print(f"\n📚 SOURCES (Filtered by Relevance ≥ {self.config.get('relevance_threshold', 0.6)}):")
        for i, source in enumerate(results['sources'], 1):
            print(f"[{i}] {source['title']} (Relevance: {source['relevance_score']:.3f})")
            print(f"    {source['url']}")
            print(f"    ({source['word_count']:,} words)")
            print()

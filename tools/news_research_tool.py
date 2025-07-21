# tools/news_research_tool.py
import requests
from crewai.tools import tool
from typing import List, Dict, Any
import os
from datetime import datetime, timedelta
import yfinance as yf

@tool("Financial News Fetcher")
def get_financial_news(keywords: str = "", category: str = "", limit: int = 10) -> str:
    """
    Fetches recent financial news articles based on keywords and category.
    
    Parameters:
    keywords (str): Keywords to search for in news articles
    category (str): Category filter (e.g., 'technology', 'healthcare', 'finance')
    limit (int): Number of articles to return (default: 10)
    
    Returns:
    str: JSON string containing news articles with title, description, url, and published date
    """
    # Using NewsAPI - you'll need to sign up for a free API key
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return "News API key not configured. Please set NEWS_API_KEY environment variable."
    
    # Build query parameters
    query_params = {
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': limit,
        'from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    }
    
    # Add keywords if provided
    if keywords:
        query_params['q'] = f"{keywords} AND (stock OR market OR finance OR investment)"
    else:
        query_params['q'] = "finance OR stock OR market OR investment"
    
    # Add category filter if provided
    if category:
        query_params['q'] += f" AND {category}"
    
    try:
        response = requests.get(
            'https://newsapi.org/v2/everything',
            params=query_params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for article in data.get('articles', []):
            if article.get('title') and article.get('description'):
                articles.append({
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'published_at': article['publishedAt'],
                    'source': article.get('source', {}).get('name', 'Unknown')
                })
        
        return str(articles)
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {str(e)}"

@tool("Stock Market News")
def get_stock_specific_news(stock_symbol: str, limit: int = 5) -> str:
    """
    Fetches news specifically related to a stock symbol.
    
    Parameters:
    stock_symbol (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA')
    limit (int): Number of articles to return
    
    Returns:
    str: News articles related to the specific stock
    """
    try:
        ticker = yf.Ticker(stock_symbol)
        news = ticker.news
        
        if not news:
            return f"No recent news found for {stock_symbol}"
        
        articles = []
        for item in news[:limit]:
            articles.append({
                'title': item.get('title', ''),
                'publisher': item.get('publisher', ''),
                'link': item.get('link', ''),
                'published': item.get('providerPublishTime', ''),
                'type': item.get('type', '')
            })
        
        return str(articles)
    
    except Exception as e:
        return f"Error fetching stock news for {stock_symbol}: {str(e)}"

@tool("Market Sector News")
def get_sector_news(sector: str, limit: int = 8) -> str:
    """
    Fetches news for a specific market sector.
    
    Parameters:
    sector (str): Market sector (e.g., 'technology', 'healthcare', 'finance')
    limit (int): Number of articles to return
    
    Returns:
    str: News articles related to the sector
    """
    sector_keywords = {
        'technology': 'technology tech software AI cloud',
        'healthcare': 'healthcare pharma biotech medical',
        'finance': 'finance banking fintech insurance',
        'energy': 'energy oil gas renewable solar',
        'consumer': 'consumer retail e-commerce automotive',
        'real_estate': 'real estate REIT property construction',
        'telecommunications': 'telecom wireless 5G network'
    }
    
    keywords = sector_keywords.get(sector.lower(), sector)
    return get_financial_news(keywords=keywords, limit=limit)

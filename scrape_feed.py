#!/usr/bin/env python3
"""
Mercer HR Content RSS Feed Scraper
Scrapes articles from Mercer's HR View Content page and generates an RSS feed.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Configuration
BASE_URL = "https://taap.mercer.com/en-us/resources/hr-view-content/"
MAX_PAGES = 3  # Scrape first 3 pages (30 most recent articles)
DELAY_SECONDS = 1  # Delay between page requests

def scrape_articles(max_pages=MAX_PAGES):
    """
    Scrape articles from Mercer HR content pages.
    
    Args:
        max_pages: Number of pages to scrape (default: 3)
    
    Returns:
        List of article dictionaries with title, link, and description
    """
    articles = []
    seen_links = set()
    
    print(f"Starting scrape of {max_pages} pages...")
    
    for page_num in range(1, max_pages + 1):
        # Construct URL for pagination
        if page_num == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}?page={page_num}"
        
        print(f"Scraping page {page_num}: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all article links
            article_links = soup.find_all('a', href=lambda x: x and '/apps/ppa/article/' in x)
            
            page_count = 0
            for link in article_links:
                article_url = link.get('href')
                
                # Make URL absolute if it's relative
                if article_url.startswith('/'):
                    article_url = f"https://taap.mercer.com{article_url}"
                
                # Ensure URL has proper protocol
                if not article_url.startswith('http'):
                    article_url = f"https://taap.mercer.com{article_url}"
                
                # Clean up any potential issues (remove fragments, extra slashes)
                article_url = article_url.strip()
                
                # Skip duplicates
                if article_url in seen_links:
                    continue
                
                seen_links.add(article_url)
                
                # Extract title (link text)
                title = link.get_text(strip=True)
                
                # Try to find description (usually in nearby paragraph or div)
                description = ""
                parent = link.find_parent()
                if parent:
                    desc_elem = parent.find('p') or parent.find('div', class_='description')
                    if desc_elem:
                        description = desc_elem.get_text(strip=True)
                
                if not description:
                    description = title  # Fallback to title
                
                articles.append({
                    'title': title,
                    'link': article_url,
                    'description': description
                })
                page_count += 1
            
            print(f"  Found {page_count} articles on page {page_num}")
            
            # Rate limiting - be respectful to the server
            if page_num < max_pages:
                time.sleep(DELAY_SECONDS)
                
        except requests.RequestException as e:
            print(f"Error scraping page {page_num}: {e}")
            continue
    
    print(f"\nTotal articles scraped: {len(articles)}")
    return articles

def escape_xml(text):
    """Escape special XML characters"""
    if not text:
        return ""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))

def generate_rss_feed(articles, output_file='mercer_feed.xml'):
    """
    Generate RSS 2.0 XML feed from articles with HTML support in descriptions.
    
    Args:
        articles: List of article dictionaries
        output_file: Output filename for RSS feed
    """
    
    # Build RSS feed manually to support CDATA for HTML content
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<rss version="2.0">')
    xml_lines.append('  <channel>')
    xml_lines.append(f'    <title>Mercer TAAP Blog</title>')
    xml_lines.append(f'    <link>{BASE_URL}</link>')
    xml_lines.append(f'    <description>Latest HR articles, alerts, and legislative updates from Mercer TAAP</description>')
    xml_lines.append(f'    <language>en-us</language>')
    xml_lines.append(f'    <lastBuildDate>{datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>')
    
    # Add articles as items
    for article in articles:
        xml_lines.append('    <item>')
        xml_lines.append(f'      <title>{escape_xml(article["title"])}</title>')
        xml_lines.append(f'      <link>{escape_xml(article["link"])}</link>')
        
        # Use CDATA for description to allow HTML content
        desc_html = f'{escape_xml(article["description"])}'
        xml_lines.append(f'      <description><![CDATA[{desc_html}]]></description>')
        
        xml_lines.append(f'      <guid isPermaLink="true">{escape_xml(article["link"])}</guid>')
        xml_lines.append(f'      <pubDate>{datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}</pubDate>')
        xml_lines.append('    </item>')
    
    xml_lines.append('  </channel>')
    xml_lines.append('</rss>')
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    print(f"\nRSS feed generated: {output_file}")
    print(f"Total items in feed: {len(articles)}")

def main():
    """Main execution function."""
    print("=" * 60)
    print("Mercer HR Content RSS Feed Generator")
    print("=" * 60)
    print()
    
    # Scrape articles
    articles = scrape_articles(max_pages=MAX_PAGES)
    
    if not articles:
        print("No articles found. Check the website structure or your internet connection.")
        return
    
    # Generate RSS feed
    generate_rss_feed(articles)
    
    print("\n" + "=" * 60)
    print("Feed generation complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()

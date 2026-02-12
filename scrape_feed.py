#!/usr/bin/env python3
"""
Mercer HR Content RSS Feed Scraper
Scrapes articles from Mercer's HR View Content page and generates an RSS feed.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import xml.etree.ElementTree as ET

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

def generate_rss_feed(articles, output_file='mercer_feed.xml'):
    """
    Generate RSS 2.0 XML feed from articles.
    
    Args:
        articles: List of article dictionaries
        output_file: Output filename for RSS feed
    """
    # Create RSS root element
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    
    # Channel metadata
    ET.SubElement(channel, 'title').text = 'Mercer TAAP Blog Posts'
    ET.SubElement(channel, 'link').text = BASE_URL
    ET.SubElement(channel, 'description').text = 'Latest HR articles, alerts, and legislative updates from Mercer'
    ET.SubElement(channel, 'language').text = 'en-us'
    ET.SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Add articles as items
    for article in articles:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = article['title']
        ET.SubElement(item, 'link').text = article['link']
        description_with_link = f"{article['description']}<br/><br/><a href=\"{article['link']}\">Read full article</a>"
        ET.SubElement(item, 'description').text = description_with_link
        ET.SubElement(item, 'guid', isPermaLink='true').text = article['link']
        ET.SubElement(item, 'pubDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Create tree and write to file
    tree = ET.ElementTree(rss)
    ET.indent(tree, space='  ')  # Pretty print
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
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

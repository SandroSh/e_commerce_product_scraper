from datetime import datetime
import logging
import os
from typing import Dict, List
from bs4 import BeautifulSoup
from request_module import fetch_webpage
from utils import absolute_url


def parse_html(html_content):
    try:
        if not html_content:
            raise ValueError("HTML content is empty or None.")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    
    except ValueError as ve:
        print(f"Error: {ve}")
        return None
    except Exception as e:
        print(f"Failed to parse HTML content: {str(e)}")
        return None


def scrape_links(soup, url):
    try:
        if not soup:
            raise ValueError("Invalid BeautifulSoup object. Cannot scrape products.")

        image_divs = soup.find_all('div', class_='image_container')
        if not image_divs:
            raise ValueError("No product items found with the specified classes.")
        
        links = []
        
        for div in image_divs:
            try:
                link_tag = div.find('a')
                href = link_tag['href'].strip() if link_tag and 'href' in link_tag.attrs else "Href not found"
            
                links.append(absolute_url(base_url=url, relative_url=href))
                
            except Exception as e:
                print(f"Error scraping product item: {str(e)}. Skipping this item.")
                continue
            
    except ValueError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"Failed to scrape products: {str(e)}")
        return []
    return links


def scrape_products(soup):
    try:
        if not soup:
            raise ValueError("Invalid BeautifulSoup object. Cannot scrape products.")

        product_items = soup.find_all('li', class_=['col-xs-6', 'col-sm-4', 'col-md-3', 'col-lg-3'])
        if not product_items:
            raise ValueError("No product items found with the specified classes.")

        products = []

        for item in product_items:
            try:
                title_tag = item.find('h3')  
                if not title_tag:
                    title_tag = item.find('p', class_='star-rating')
                    if title_tag:
                        title_tag = title_tag.find_next('h3') or title_tag.find_next('a')

                title = title_tag.text.strip() if title_tag else "Title not found"

                
                price_tag = item.find('p', class_='price_color')
                price = price_tag.text.strip() if price_tag else "Price not found"

             
                products.append({
                    'title': title,
                    'price': price
                })

            except Exception as e:
                print(f"Error scraping product item: {str(e)}. Skipping this item.")
                continue

        return products

    except ValueError as ve:
        print(f"Error: {ve}")
        return []
    except Exception as e:
        print(f"Failed to scrape products: {str(e)}")
        return []






if __name__ == "__main__":
    url = "https://books.toscrape.com/"
    response = fetch_webpage(url)
    html_content = parse_html(response)
    links = scrape_links(html_content, url)
    
    

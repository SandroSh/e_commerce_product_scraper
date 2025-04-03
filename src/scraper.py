from bs4 import BeautifulSoup
from request_module import fetch_webpage
from utils import absolute_url
from utils import extract_number, save_list_to_csv


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

        product_item = soup.find('div', class_='product_main')
        if not product_item:
            raise ValueError("No product items found with the specified classes.")

       
        title_tag = product_item.find('h1')
        if not title_tag:
            title_tag = product_item.find('p', class_='star-rating')
            if title_tag:
                title_tag = title_tag.find_next('h1') or title_tag.find_next('a')
        title = title_tag.text.strip() if title_tag else "Title not found"

    
        price_tag = product_item.find('p', class_='price_color')
        price = price_tag.text.strip() if price_tag else "Price not found"

      
        description_tag = soup.find('div', class_='sub-header').find_next('p') 
        description = description_tag.text.strip() if description_tag else "Description not found"

        tables = soup.find('table', class_='table table-striped')
        
        tr_elements = tables.find_all('tr')
        
        upc_code = tr_elements[0].text.strip() if tr_elements[0] else 'upc code not found'
        
        product_type = tr_elements[1].text.strip() if tr_elements[1] else 'product type not found'
        
        in_stock = tr_elements[5].text.strip() if tr_elements[5] else 'product stock not found'
        
        reviews = tr_elements[6].text.strip() if tr_elements[6] else 'product reviews not found'
        
        index = reviews.find("reviews")
        reviews = reviews[index + 8:]

        products = [{
            'title': title,
            'price': float(price[1:]),
            'description': description,
            'upc_code':upc_code,
            'type':product_type,
            'in_stock':extract_number(in_stock),
            'reviews': int(reviews)
        }]

        return products

    except ValueError as ve:
        print(f"Error: {ve}")
        return []
    except Exception as e:
        print(f"Failed to scrape products: {str(e)}")
        return []

def scrape_products_with_details(links):
    try:
        if not links:
            raise ValueError("Invalid BeautifulSoup object. Cannot scrape products.")
        
        products = []
        for link in links:
            try:
               response = fetch_webpage(link)
               html_content = parse_html(response)
               product = scrape_products(html_content)
               products.append(product) 
               
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
    products = scrape_products_with_details(links)
    save_list_to_csv('product_books.csv', products)
    

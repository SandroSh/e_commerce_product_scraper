# 📚 Book Scraper – Python Web Scraper for [Books to Scrape](https://books.toscrape.com/)

This Python project scrapes product data from [books.toscrape.com](https://books.toscrape.com/), extracts useful information like title, price, stock, and reviews, and saves the data in both **CSV** and **JSON** formats.

---

## 🚀 Features

- Scrapes book details from the homepage and linked product pages.
- Parses product title, price, description, UPC, stock availability, and review count.
- Saves the data in both `.csv` and `.json` files inside a `data/` directory.

---
## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/SandroSh/e_commerce_product_scraper.git
cd e_commerce_product_scraper
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
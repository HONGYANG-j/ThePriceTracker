import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def run_price_tracker():
    print("🕷️ Initiating Competitor Price Scraper...")
    
    # Target URL (A safe sandbox site built for scraping practice)
    url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    
    # Disguise our script as a normal web browser
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    print(f"📡 Connecting to target website...")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all product containers
    products = soup.find_all('article', class_='product_pod')
    
    scraped_data = []
    
    for item in products:
        # Extract product title
        title = item.h3.a['title']
        
        # Extract price and clean the currency symbol
        price_text = item.find('p', class_='price_color').text
        clean_price = float(price_text.replace('£', ''))
        
        # Add to our data list
        scraped_data.append({'Product_Name': title, 'Price': clean_price})
        
    # Convert to a data table (using your Pandas skills)
    df = pd.DataFrame(scraped_data)
    
    # Advanced logic: Flag any product priced under 40 as a "Price Drop Alert"
    df['Status'] = df['Price'].apply(lambda x: '🚨 ALERT: Underpriced' if x < 40 else 'Normal')
    
    # Save the intel
    os.makedirs("output", exist_ok=True)
    output_path = "output/competitor_pricing_intel.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Successfully extracted pricing for {len(products)} products!")
    print(f"📊 Market intelligence report saved to: {output_path}")

if __name__ == "__main__":
    run_price_tracker()

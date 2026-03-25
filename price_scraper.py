import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# 1. Fetch Cloud Secrets (Securely getting Telegram credentials)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials missing in environment. Skipping alert.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
        print("📲 BOOM! Telegram push notification sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")

def run_price_tracker():
    print("🕷️ Initiating Competitor Price Scraper & Watchdog...")
    
    url = "https://books.toscrape.com/catalogue/category/books/science_22/index.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('article', class_='product_pod')
    
    scraped_data = []
    alert_messages = [] # Container for our emergency alerts
    
    for item in products:
        title = item.h3.a['title']
        price_text = item.find('p', class_='price_color').text
        clean_price = float(price_text.replace('£', '').replace('Â', ''))
        scraped_data.append({'Product_Name': title, 'Price': clean_price})
        
        # CORE LOGIC: If price drops below £40, trigger the alarm!
        if clean_price < 40:
            alert_messages.append(f"🚨 *PRICE DROP:* {title} is now *£{clean_price}*")
            
    df = pd.DataFrame(scraped_data)
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/competitor_pricing_intel.csv", index=False)
    
    print(f"✅ Extracted pricing for {len(products)} products.")
    
    # 2. The Final Strike: Send the alert if targets are found
    if alert_messages:
        print("🔔 Underpriced items detected! Triggering Telegram Bot...")
        final_message = "📉 *COMPETITOR PRICE ALERT*\n\n" + "\n".join(alert_messages)
        send_telegram_alert(final_message)
    else:
        print("✅ All competitor prices are within normal range. No alerts triggered.")

if __name__ == "__main__":
    run_price_tracker()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
import schedule
import time
from datetime import datetime
import csv  # For CSV logging
import os   # To check if file exists

# --- Email alert function ---
def send_email_alert(product_title, product_price, product_url):
    sender_email = "sandhya777771@gmail.com"
    sender_password = "tkap kaeu qyib fwqp"  # Use Gmail App Password
    receiver_email = "sandhya777771@gmail.com"

    subject = f"Price Alert: {product_title}"
    body = f"The price has dropped to {product_price}!\nCheck it here: {product_url}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_email, msg.as_string())

    print(f"✅ Alert email sent for '{product_title}'!")

# --- Log price history to CSV ---
def log_price_to_csv(timestamp, product_title, product_price, product_url):
    file_exists = os.path.isfile("price_history.csv")
    with open("price_history.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "Product Title", "Price", "URL"])
        writer.writerow([timestamp, product_title, product_price, product_url])

# --- Price check and scrape function ---
def check_price(product):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
    wait = WebDriverWait(driver, 10)

    product_url = product["url"]
    price_threshold = product["threshold"]
    driver.get(product_url)

    try:
        title_element = wait.until(EC.presence_of_element_located((By.ID, "productTitle")))
        product_title = title_element.text.strip()
        print("✅ Product Title:", product_title)
    except Exception as e:
        print("❌ Product title not found:", e)
        product_title = "Unknown Product"

    try:
        price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-price > span.a-offscreen")))
        price_str = price_element.get_attribute("innerText").strip()
        print("✅ Product Price:", price_str)
    except Exception as e:
        print("❌ Product price not found:", e)
        price_str = None

    # Log to file
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - Checked '{product_title}' at {price_str}\n")

    # Log to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_price_to_csv(timestamp, product_title, price_str if price_str else "N/A", product_url)

    if price_str:
        try:
            price_num = float(price_str.replace('₹', '').replace(',', ''))
        except Exception as e:
            print(f"❌ Could not convert price to float: {e}")
            price_num = None

        if price_num is not None:
            if price_num < price_threshold:
                send_email_alert(product_title, price_str, product_url)
            else:
                print(f"Price is still above threshold: {price_str}")
        else:
            print("Price comparison skipped due to conversion error.")
    else:
        print("No price found to compare.")
    
    driver.quit()

# --- List of products to track ---
products = [
    {
        "url": "https://www.amazon.in/HP-AI-Powered-16-1-inch-Backlit-xf0100AX/dp/B0D1BT9SXF/",
        "threshold": 200000
    },
    {
        "url": "https://www.amazon.in/dp/B0DZD8QJBH?th=1",  # Replace with valid URL
        "threshold": 120000
    },
]

# --- Scheduled job to check all products ---
def job():
    print(f"Checking products at {datetime.now()}...\n")
    for product in products:
        print(f"Checking product: {product['url']}")
        check_price(product)
        print("-" * 40)

schedule.every(1).hour.do(job)

print("Starting price tracker... (checks every hour)")
job()  # Initial run

while True:
    schedule.run_pending()
    time.sleep(1)
    
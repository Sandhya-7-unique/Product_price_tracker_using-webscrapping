📌 Project Title:
Product Price Tracker using Python, Selenium & WebDriver

🧩 Objective:
To automatically monitor the price of a specific product on an e-commerce website (e.g., Amazon), and alert the user when the price falls below a predefined threshold.

🛠️ Technology Stack:
Language: Python

Libraries:

Selenium – for web scraping dynamic content

time – to control script execution and delays

smtplib (optional) – to send email notifications

Tools: Chrome browser and ChromeDriver

📖 How It Works:
Setup Selenium WebDriver:
Launches a Chrome browser session using Selenium WebDriver.

Navigate to Product Page:
The script opens a product page (e.g., an Amazon product link) provided in the URL.

Extract Product Data:
It locates and extracts the product title and current price using HTML element identifiers like ID, class, etc.

Compare with Threshold:
It compares the current price with a user-defined target price.

Alert the User:

If the price is less than the threshold, it prints a message or triggers an email alert.

If not, it just reports the current price and exits.

Exit Cleanly:
The browser is closed using driver.quit() to free system resources. 

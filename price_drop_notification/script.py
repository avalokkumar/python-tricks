import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Amazon search URL template
AMAZON_SEARCH_URL = 'https://www.amazon.in/s?k={}'

# Keywords to search for products
keywords = ['laptop', 'headphones', 'smartphone']

# Threshold for price drop notification (in percentage)
price_drop_threshold = 10

# Email configuration
sender_email = 'amazon-support@amazon.in'
receiver_email = 'test@gmail.com'
email_password = 'Test@123'

# User-Agent for headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch_product_details(keyword):
    """Fetch product details from Amazon using the keyword."""
    search_url = AMAZON_SEARCH_URL.format(keyword.replace(' ', '+'))
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product details
    product_elements = soup.find_all('div', {'data-component-type': 's-search-result'})
    products = []

    for element in product_elements:
        try:
            # Extract product title
            title = element.h2.text.strip()

            # Extract price; handling various formats
            price_whole = element.find('span', 'a-price-whole')
            price_fraction = element.find('span', 'a-price-fraction')
            if price_whole and price_fraction:
                price = float(price_whole.text.replace(',', '') + '.' + price_fraction.text)
            else:
                continue

            # Extract product link
            link = 'https://www.amazon.in' + element.h2.a['href']
            
            # Store product details
            products.append({
                'title': title,
                'price': price,
                'link': link
            })

        except AttributeError:
            continue  # Skip items that don't have complete data

    return products

def send_notification(product, old_price, new_price):
    """Send an email notification for the price drop."""
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f'Price Drop Alert: {product["title"]}'

    body = (
        f'The price of "{product["title"]}" has dropped from ₹{old_price} to ₹{new_price}.\n'
        f'Check it out here: {product["link"]}'
    )
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def monitor_prices():
    """Monitor Amazon for price drops."""
    previous_prices = {}

    while True:
        for keyword in keywords:
            products = fetch_product_details(keyword)
            
            for product in products:
                if product['link'] in previous_prices:
                    old_price = previous_prices[product['link']]
                    new_price = product['price']

                    # Calculate the percentage price drop
                    price_drop = ((old_price - new_price) / old_price) * 100

                    # Notify if the price drop exceeds the threshold
                    if price_drop >= price_drop_threshold:
                        send_notification(product, old_price, new_price)

                # Update the price record
                previous_prices[product['link']] = product['price']

        # Wait for an hour before checking again
        time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    monitor_prices()
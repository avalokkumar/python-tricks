import os
import time
import requests
import logging
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(filename='logs/scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 2Captcha API Key from environment variables
API_KEY = os.getenv('CAPTCHA_API_KEY')


# Function to setup Selenium with headless mode and proxies
def setup_browser(headless=True, proxy=None):
    options = Options()
    if headless:
        options.add_argument('--headless')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    return driver


# Function to solve CAPTCHA using 2Captcha
def solve_captcha_2captcha(driver, captcha_xpath):
    solver = TwoCaptcha(API_KEY)

    # Find CAPTCHA element and get its source URL
    captcha_element = driver.find_element(By.XPATH, captcha_xpath)
    captcha_image_url = captcha_element.get_attribute('src')

    # Download CAPTCHA image locally
    captcha_image_path = 'captcha.png'
    img_data = requests.get(captcha_image_url).content
    with open(captcha_image_path, 'wb') as handler:
        handler.write(img_data)

    # Solve the CAPTCHA using 2Captcha
    try:
        result = solver.normal(captcha_image_path)
        return result['code']
    except Exception as e:
        logging.error(f'Error solving CAPTCHA: {e}')
        return None


# Function to scrape dynamic content and handle CAPTCHA
def scrape_website(url, use_2captcha, captcha_xpath, output_file, proxy=None, headless=True):
    driver = setup_browser(headless=headless, proxy=proxy)
    driver.get(url)

    # Handle CAPTCHA if present
    if use_2captcha:
        logging.info('CAPTCHA detected, attempting to solve it...')
        captcha_solution = solve_captcha_2captcha(driver, captcha_xpath)
        if captcha_solution:
            # Enter CAPTCHA solution and submit
            captcha_input = driver.find_element(By.XPATH, captcha_xpath)
            captcha_input.send_keys(captcha_solution)
            captcha_input.send_keys(Keys.RETURN)
            time.sleep(5)  # Wait for CAPTCHA validation
        else:
            logging.error('Failed to solve CAPTCHA.')
            driver.quit()
            return

    # Wait for dynamic content to load
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Extract content with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find data (adjust selectors based on the target website)
    data = []
    for element in soup.find_all('div', class_='target-class'):
        data.append({
            'title': element.find('h1').get_text(strip=True),
            'description': element.find('p').get_text(strip=True)
        })

    # Write scraped data to a file
    with open(output_file, 'w') as f:
        f.write(str(data))

    logging.info(f'Data saved to {output_file}')
    driver.quit()


# Main function to handle arguments
def main():
    parser = argparse.ArgumentParser(description="Web scraper with CAPTCHA bypass")
    parser.add_argument('--url', required=True, help="URL of the website to scrape")
    parser.add_argument('--output', required=True, help="Output file to save scraped data")
    parser.add_argument('--use_2captcha', action='store_true', help="Use 2Captcha to bypass CAPTCHA")
    parser.add_argument('--proxy', help="Use a proxy for the scraper (format: http://ip:port)")
    parser.add_argument('--captcha_xpath', help="XPath of the CAPTCHA input element", default="")
    parser.add_argument('--headless', action='store_true', help="Run browser in headless mode")
    args = parser.parse_args()

    scrape_website(args.url, args.use_2captcha, args.captcha_xpath, args.output, args.proxy, args.headless)


if __name__ == '__main__':
    main()
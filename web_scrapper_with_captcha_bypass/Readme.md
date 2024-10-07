# Web Scraper with CAPTCHA Bypass

## Overview
`web_scraper.py` is a Python-based web scraper designed to handle dynamic content and bypass CAPTCHAs. It uses services like 2Captcha and can be extended to incorporate machine learning (ML) models for CAPTCHA solving. This scraper handles web pages that use JavaScript to load content and can navigate through sites that implement CAPTCHA as a defense mechanism.

## Features
- **Dynamic Content Handling**: Leverages Selenium or Puppeteer to load and scrape content from web pages that rely on JavaScript.
- **CAPTCHA Bypass**: Supports bypassing CAPTCHA challenges using:
  - **2Captcha**: An external service for solving image-based and reCAPTCHA CAPTCHAs.
  - **Custom ML Models**: Extend the solution with custom models trained to recognize and solve specific CAPTCHA challenges.
- **Proxy Support**: Integrates with proxies to avoid IP blocking.
- **Headless Mode**: Operates in headless mode to make the scraper faster and less detectable.
- **User-Agent Rotation**: Randomizes User-Agent headers to avoid detection.
- **HTML Parsing**: Uses `BeautifulSoup` to parse and extract structured data from HTML.
- **Logging**: Implements logging for better debugging and result tracking.
  
## Installation

### Prerequisites
- **Python 3.x**
- **Selenium** or **Playwright**
- **BeautifulSoup4**
- **2Captcha API Key** (if using 2Captcha service)

### Required Python Libraries

```txt
selenium
beautifulsoup4
requests
2captcha-python
playwright
undetected-chromedriver
```

### Browser Drivers
If you're using Selenium, make sure to install a browser driver compatible with your browser (e.g., ChromeDriver for Chrome).

For Playwright:
```bash
pip install playwright
playwright install
```

### 2Captcha API
To use the 2Captcha service, sign up on [2Captcha](https://2captcha.com/), and get an API key. You’ll need this to solve CAPTCHAs.

## Setup

1. **2Captcha Configuration**:
   - Obtain your API key from 2Captcha.
   - Set it in an environment variable or pass it as an argument in the script.
   
   Example:
   ```bash
   export CAPTCHA_API_KEY="your_2captcha_api_key"
   ```

2. **Custom ML CAPTCHA Solving**:
   If you have an ML model for CAPTCHA solving, integrate it into the `solve_captcha_ml()` function, which will take the CAPTCHA image as input and return the solved CAPTCHA.

## Usage

### Command Line Arguments
You can run the scraper from the command line with different arguments:

```bash
python web_scraper.py --url "https://example.com" --output "data.json" --use_2captcha --proxy "http://proxy_ip:port"
```

| Argument        | Description                                                           |
|-----------------|-----------------------------------------------------------------------|
| `--url`         | URL of the website to scrape.                                         |
| `--output`      | File where the scraped data will be saved (e.g., JSON, CSV).          |
| `--use_2captcha`| Enable CAPTCHA solving using 2Captcha.                                |
| `--proxy`       | (Optional) Use a proxy for scraping.                                  |
| `--headless`    | Run browser in headless mode (default: `True`).                       |

### Example with 2Captcha
```bash
python web_scraper.py --url "https://example.com" --output "result.json" --use_2captcha --headless
```

### CAPTCHA Solving Process
1. The scraper detects if a CAPTCHA challenge is present on the page.
2. If a CAPTCHA is detected:
   - If `--use_2captcha` is enabled, the CAPTCHA image will be sent to 2Captcha for solving.
   - If a custom ML model is integrated, the CAPTCHA image will be passed to the model for solving.
3. Once the CAPTCHA is solved, the scraper submits the solution and proceeds with the scraping task.

### Using Proxies
You can use proxies to prevent your IP from being blocked while scraping multiple pages:
```bash
python web_scraper.py --url "https://example.com" --output "result.json" --proxy "http://proxy_ip:port"
```

### Handling Dynamic Content
The scraper uses Selenium or Playwright to handle pages that load content dynamically via JavaScript. It waits until the required elements are loaded before extracting the data.

### Logging
Logs will be saved in the `logs/` directory by default. To enable more detailed logging, modify the logging level in `web_scraper.py`.

## Customizing the Scraper

### CAPTCHA Solver Using ML
To implement a custom ML CAPTCHA solver:
1. Replace the logic inside the `solve_captcha_ml()` function.
2. Pass the CAPTCHA image to your ML model.
3. Return the solved CAPTCHA string for submission.

Example:
```python
def solve_captcha_ml(captcha_image_path):
    # Load your ML model and solve the CAPTCHA
    solution = your_ml_model.predict(captcha_image_path)
    return solution
```

### Extending the Scraper
You can extend the scraper by adding more functionality such as:
- Scraping data from multiple URLs in parallel.
- Implementing different strategies for avoiding bot detection.
- Integrating other CAPTCHA solving services.

## Limitations
- CAPTCHA bypass is dependent on the service or model used. Solving complex CAPTCHAs may take time or fail if the model or service is inadequate.
- Websites with advanced bot detection mechanisms may require additional strategies like better proxy rotation, cookies management, or more sophisticated user-agent management.

## Future Enhancements
- Add more CAPTCHA solving services (e.g., Anti-Captcha).
- Improve the ML model's accuracy for CAPTCHA solving.
- Implement scraping of large websites using distributed systems like Scrapy and Celery.

## Acknowledgments
- [2Captcha](https://2captcha.com) for their CAPTCHA solving service.
- [Selenium](https://www.selenium.dev/) and [Playwright](https://playwright.dev/) for browser automation.

---

## Running the script

```
python web_scraper.py --url "https://example.com" --output "output.json" --use_2captcha --captcha_xpath "//input[@id='captcha']"
```
## **Amazon Price Drop Monitoring Script**

This Python script monitors product prices on Amazon.in based on provided keywords and sends an email notification when a price drop is detected. It fetches product details, compares prices, and triggers an alert if the price drops beyond a specified threshold.

### **Prerequisites**

Before running the script, ensure you have the following:

1. **Python 3.x** installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
   
2. **Required Python Libraries**: Install necessary libraries using pip:
   ```bash
   pip install requests beautifulsoup4
   ```

3. **Email Account for Notifications**:
   - A valid email account (Gmail, Yahoo, etc.) to send notifications.
   - For Gmail accounts, ensure that "Less secure app access" is enabled, or generate an App Password if using 2-step verification.

### **Step-by-Step Setup Guide**

1. **Clone the Repository or Download the Script**:
   Download the Python script `script.py` or clone the repository to your local machine.

2. **Configure Email Settings**:
   - Open the script in a text editor.
   - Update the email configuration section with your credentials:
     ```python
     sender_email = 'your_email@example.com'       # Your email address
     receiver_email = 'receiver_email@example.com' # Email address to receive notifications
     email_password = 'your_email_password'        # Your email password or app password
     ```

3. **Set Your Search Keywords and Price Drop Threshold**:
   - Adjust the `keywords` list in the script to include the products you want to monitor:
     ```python
     keywords = ['laptop', 'headphones', 'smartphone']
     ```
   - Set the `price_drop_threshold` variable to define the percentage drop needed to trigger a notification:
     ```python
     price_drop_threshold = 10  # Example: 10% drop
     ```

4. **Run the Script**:
   - Open your terminal or command prompt.
   - Navigate to the directory where the script is located.
   - Run the script using Python:
     ```bash
     python amazon_price_monitor.py
     ```

### **How the Script Works**

1. **Fetch Product Details**: The script uses BeautifulSoup to scrape product details like title, price, and link from Amazon based on the provided keywords.

2. **Monitor Prices**: 
   - It runs an infinite loop, checking product prices periodically (every hour).
   - If the current price of a product drops below the previous recorded price by the defined threshold, an email notification is sent.

3. **Send Email Notifications**: 
   - The script sends an email alert with the product name, old price, new price, and a link to the product page whenever a significant price drop is detected.

### **Handling Errors and Troubleshooting**

- **No Products Found**: If the script does not fetch any products, verify that the keywords are correct and check if the HTML selectors used in the script match Amazon's current layout.
  
- **Email Sending Issues**: 
  - Ensure that the sender's email account settings allow SMTP access.
  - Check that the email credentials are correctly entered in the script.

- **Blocked Access by Amazon**: 
  - To avoid getting blocked, ensure the script runs with a delay between requests (already set to 1 hour).
  - Keep the number of requests to a minimum to comply with Amazon’s terms of service.

### **Disclaimer**
This script is intended for personal use and educational purposes only. Excessive scraping of Amazon's website may violate their terms of service. Use responsibly and consider Amazon’s guidelines for automated requests.

### **Contributing**
Feel free to fork the repository and submit pull requests for improvements or additional features!

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Define your WebDriver service (adjust the path if necessary)
service = Service(executable_path='/path/to/chromedriver')  # Update with your ChromeDriver path
# ex: service = Service(executable_path='/usr/local/bin/chromedriver')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)
# driver = webdriver.Chrome()  # If the ChromeDriver is in your PATH

# Define the URL of the website with the form
url = 'https://example.com/registration'  # Replace with the actual URL
# ex: url = 'https://www.udemy.com/join/signup-popup`

def fill_form():
    try:
        # Open the target website
        driver.get(url)

        # Wait for the page to load and the form to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))  # Adjust the selector as needed
        )

        # Fill in the username field
        username = driver.find_element(By.NAME, 'username')  # Replace with the actual field name
        username.send_keys('testuser')

        # Fill in the email field
        email = driver.find_element(By.NAME, 'email')  # Replace with the actual field name
        email.send_keys('testuser@example.com')

        # Fill in the password field
        password = driver.find_element(By.NAME, 'password')  # Replace with the actual field name
        password.send_keys('securepassword')

        # Optionally, fill in other fields
        # Example: Fill in a phone number
        phone = driver.find_element(By.NAME, 'phone')
        phone.send_keys('1234567890')

        # Check a checkbox (if any)
        # Example: Accept terms and conditions checkbox
        terms_checkbox = driver.find_element(By.ID, 'terms')  # Replace with actual ID or other locator
        terms_checkbox.click()

        address = driver.find_element(By.NAME, 'address')  # Replace with the actual field name
        address.send_keys('123 Main Street')

        city = driver.find_element(By.NAME, 'city')  # Replace with the actual field name
        city.send_keys('Anytown')

        # Fill in a ZIP code
        zip_code = driver.find_element(By.NAME, 'zip')  # Replace with the actual field name
        zip_code.send_keys('12345')

        # fill the state
        state = driver.find_element(By.NAME, 'state')  # Replace with the actual field name
        state.send_keys('AnyState')

        # fill the country
        country = driver.find_element(By.NAME, 'country')  # Replace with the actual field name
        country.send_keys('AnyCountry')

        # Upload a file (if required)
        # Example: Upload a profile picture
        file_input = driver.find_element(By.ID, 'file-upload')  # Replace with the actual ID
        file_input.send_keys('/path/to/profile_picture.jpg')  # Update with the actual file path

        # Select an option from a dropdown (if any)
        # Example: Select a country from a dropdown
        country_dropdown = driver.find_element(By.ID, 'country')
        for option in country_dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == 'India':  # Replace with desired option
                option.click()
                break

        # Select a radio button (if any)
        # Example: Select a payment method
        payment_radio = driver.find_element(By.ID, 'payment-method')  # Replace with the actual ID
        payment_radio.click()

        # Click on a button to trigger an action
        # Example: Click on the 'Submit' button
        # Note: You may need to scroll to the button if it's not visible
        # driver.execute_script("arguments[0].scrollIntoView();", submit_button)  # Scroll to the element
        # submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Replace with the correct XPath

        # Submit the form
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Replace with the correct XPath
        submit_button.click()

        # Wait for a few seconds to observe the result (optional)
        time.sleep(5)

    except TimeoutException:
        print("Loading took too much time!")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    fill_form()
"""
Module to automatically submit phone numbers to spam reporting websites.
For now, submits to https://spamcallers.org/ using Selenium.
"""

import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Hardcoded phone number for testing
PHONE_NUMBER = "435-200-0096"
WEBSITE_URL = "https://spamcallers.org/"


def submit_phone_number():
    """
    Submits a phone number to the spam reporting website.
    Runs in a background thread to avoid blocking the call handling.
    """
    thread = threading.Thread(target=_submit_in_background, daemon=True)
    thread.start()


def _submit_in_background():
    """
    Background task to submit the phone number using Selenium.
    """
    try:
        print(f"[REPORT_SPAM] Starting spam report submission for {PHONE_NUMBER}")
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # Uncomment for headless mode (no window):
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize WebDriver with webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            # Navigate to website
            print(f"[REPORT_SPAM] Navigating to {WEBSITE_URL}")
            driver.get(WEBSITE_URL)
            
            # Wait for page to load and find input field
            wait = WebDriverWait(driver, 10)
            
            # Try different selectors for the phone input field
            selectors = [
                (By.NAME, "phone"),
                (By.CSS_SELECTOR, "input[name='phone']"),
                (By.CSS_SELECTOR, "input.phone"),
                (By.ID, "phone"),
                (By.CSS_SELECTOR, "input[type='text'][name='phone']"),
            ]
            
            input_field = None
            for selector in selectors:
                try:
                    print(f"[REPORT_SPAM] Trying selector: {selector}")
                    input_field = wait.until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"[REPORT_SPAM] Found input field with selector: {selector}")
                    break
                except Exception as e:
                    print(f"[REPORT_SPAM] Selector {selector} failed: {e}")
                    continue
            
            if not input_field:
                print("[REPORT_SPAM] Could not find phone input field")
                return
            
            # Enter phone number
            print(f"[REPORT_SPAM] Entering phone number: {PHONE_NUMBER}")
            input_field.clear()
            input_field.send_keys(PHONE_NUMBER)
            
            # Wait a moment for input to register
            time.sleep(0.5)
            
            # Find and click submit button
            submit_selectors = [
                (By.ID, "submit"),
                (By.CSS_SELECTOR, "button[type='button']#submit"),
                (By.CSS_SELECTOR, "button.mdc-button"),
                (By.XPATH, "//button[@id='submit']"),
                (By.XPATH, "//button[contains(text(), 'Submit')]"),
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    print(f"[REPORT_SPAM] Trying button selector: {selector}")
                    submit_button = driver.find_element(selector[0], selector[1])
                    print(f"[REPORT_SPAM] Found submit button with selector: {selector}")
                    break
                except Exception as e:
                    print(f"[REPORT_SPAM] Button selector {selector} failed: {e}")
                    continue
            
            if not submit_button:
                print("[REPORT_SPAM] Could not find submit button")
                return
            
            # Click submit button
            print("[REPORT_SPAM] Clicking submit button")
            submit_button.click()
            
            # Wait briefly for submission to complete
            time.sleep(2)
            
            print("[REPORT_SPAM] Phone number successfully submitted!")
            
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"[REPORT_SPAM] Error during submission: {e}")
        import traceback
        traceback.print_exc()

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the target website
driver.get("https://wgzimmer.ch")  # Change this to the actual URL

time.sleep(2)  # Wait for pop-up to load

try:
    # Locate the button using its class
    # consent_button = driver.find_element(By.CSS_SELECTOR, "button.fc-faq-header.fc-dialog-restricted-content")
    consent_button = driver.find_element(By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button")
    consent_button.click()
    print("Consent pop-up closed.")
except Exception as e:
    print("Consent pop-up not found or already closed.", e)
time.sleep(2)  # Wait for pop-up to load
time.sleep(2)  # Wait for pop-up to load

# Continue with further automation...

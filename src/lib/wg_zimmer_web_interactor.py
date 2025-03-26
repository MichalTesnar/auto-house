from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import re

TIME_DELAY_ON_LOAD = 2
SILENT = False

class WGZimmerWebInteractor():
    
    def __init__(self, profile):
        self.base_url = "https://www.wgzimmer.ch/wgzimmer/search/mate.html"
        self.profile = profile
    
        if SILENT:    
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome()
            
        self.next_link = None
        self.has_next_link = False
                
        self.state = "STARTING"
    
    def load(self):
        self.driver.get(self.base_url)
        time.sleep(TIME_DELAY_ON_LOAD) # Needs more time otherwise gets caught behind cookie button.
        consent_button = self.driver.find_element(By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button")
        consent_button.click()
        time.sleep(TIME_DELAY_ON_LOAD)
        self.state = "LOADED"
    
    def enter(self):
        # Select minimum price
        price_min_dropdown = self.driver.find_element(By.NAME, "priceMin")
        for option in price_min_dropdown.find_elements(By.TAG_NAME, "option"):
            if option.get_attribute("value") == "200":
                option.click()
                break

        # Select maximum price
        price_max_dropdown = self.driver.find_element(By.NAME, "priceMax")
        for option in price_max_dropdown.find_elements(By.TAG_NAME, "option"):
            if option.get_attribute("value") == str(self.profile.max_rent_wg_zimmer):
                option.click()
                break

        # Select region
        region_dropdown = self.driver.find_element(By.NAME, "wgState")
        for option in region_dropdown.find_elements(By.TAG_NAME, "option"):
            if option.get_attribute("value") == self.profile.place_wg_zimmer:
                option.click()
                break

        # time.sleep(TIME_DELAY_ON_LOAD)
        self.state = "FORM_FILLED"
    
    def search(self):
        search_field = self.driver.find_element(By.NAME, "query")
        search_field.send_keys(Keys.RETURN)
        time.sleep(TIME_DELAY_ON_LOAD)
        self.state = "ENTERED"
        
    def gather_results(self):
        # Get all links
        links = self.driver.find_elements(By.XPATH, '//a[@href]')
        # Filter
        for link in links:
            url = link.get_attribute('href')
            if "https://www.wgzimmer.ch/wglink/" in url and "facebook" not in url:
                self.next_link = url
                self.has_next_link = True
                
        self.state = "GOT LINKS"
        return
    
    def visit_and_gather(self):
        match = re.search(r'/de/([a-z0-9\-]+)/', self.next_link)
        pid = match.group(1)
        
        
        print(self.next_link)
        self.driver.get(self.next_link)
        time.sleep(TIME_DELAY_ON_LOAD)
        
        elements_to_extract = [
            "date-cost",
            "adress-region",
            "mate-content nbb",
            "room-content",
            "person-content"
        ]
        
        extracted_content = ""
        for class_name in elements_to_extract:
            try:
                element = self.driver.find_element(By.XPATH, f"//div[contains(@class, '{class_name}')]/p").text
                extracted_content += element + " "
            except Exception as e:
                html_content = "1"
                extracted_content += html_content
        
        extracted_content
        
        next_link_element = self.driver.find_element(By.CLASS_NAME, "next")
        self.next_link = next_link_element.get_attribute('href')
            
        return pid, extracted_content
    
    def send_information(self, message):
        
        # Locate and click the button to reveal contact details
        contact_button = self.driver.find_element(By.XPATH, "//a[contains(@onclick, 'showContactDetail')]")
        contact_button.click()
        time.sleep(TIME_DELAY_ON_LOAD)
        
        user_name_field = self.driver.find_element(By.ID, "senderName")
        user_name_field.send_keys(self.profile.user_name)
        
        email_field = self.driver.find_element(By.ID, "senderEmail")
        email_field.send_keys(self.profile.user_email)
        
        phone_field = self.driver.find_element(By.ID, "senderPhone")
        phone_field.send_keys(self.profile.user_phone_number)
        
        text_field = self.driver.find_element(By.ID, "senderText")
        text_field.send_keys(message)
        
        send_button = self.driver.find_element(By.CLASS_NAME, "submit-inline-mail")
        send_button.click()
        
    def close(self):
        self.driver.quit()
    
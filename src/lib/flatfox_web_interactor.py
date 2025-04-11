from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import re

from selenium.webdriver.common.action_chains import ActionChains


TIME_DELAY_ON_LOAD = 0.5
SILENT = False # use driver.get_screenshot_as_file("capture.png") to debug

class FlatfoxWebInteractor():
    
    def __init__(self, profile, email_client):
        self.base_url = "https://flatfox.ch/en/accounts/login/?next=/en/search/"
        self.profile = profile
        self.email_client = email_client
        self.driver = webdriver.Chrome()
        self.state = "STARTING"
        
    
    def load(self):
        self.driver.get(self.base_url)
        time.sleep(TIME_DELAY_ON_LOAD)
        consent_button = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
        consent_button.click()
        time.sleep(TIME_DELAY_ON_LOAD)
        self.state = "LOADED"
    
    def enter(self):
        username_field = self.driver.find_element(By.ID, "id_email")
        username_field.send_keys(self.profile.flatfox_login)
        consent_button = self.driver.find_element(By.CLASS_NAME, "css-1iioj0r")
        consent_button.click()
        time.sleep(TIME_DELAY_ON_LOAD)
        username_field = self.driver.find_element(By.ID, "id_password")
        username_field.send_keys(self.profile.flatfox_password)
        consent_button.click()
        time.sleep(4) # give email some time to arrive
        code = self.email_client.retrieve_6digit_code()
        otp_field = self.driver.find_element(By.ID, "f1")
        otp_field.send_keys(code)
        consent_button.click()
        self.state = "ENTERED"
    
    def search(self):
        time.sleep(1)
        
        region_field = self.driver.find_element(By.CLASS_NAME, "mapboxgl-ctrl-geocoder--input")
        region_field.send_keys(self.profile.place)
        ### LOCATION
        time.sleep(1)
        suggestion_button = self.driver.find_element(By.CLASS_NAME, "mapboxgl-ctrl-geocoder--suggestion-address")
        suggestion_button.click()
        region_field.send_keys(Keys.RETURN)
        
        ### ROOMS
        time.sleep(1)
        buttons = self.driver.find_elements(By.CLASS_NAME, "css-1mtdczm")
        buttons[0].click()
        self.driver.find_element(By.CSS_SELECTOR, 'button[value="SHARED"]').click()
        buttons[0].click() # close the search for type to be able to open the new one
        
        ### PRICE
        # buttons[2].click()
        
        # Grab the current URL the browser is at
        current_url = self.driver.current_url
        new_url = current_url + f'&max_price={self.profile.max_rent}'
        self.driver.get(new_url)
        
        time.sleep(1)
        
        # time.sleep(1)
        # price_field = self.driver.find_elements(By.CLASS_NAME, "search-bar-pricing-minmax__active")
        # time.sleep(1000)
        # price_field[0].send_keys(0)
        # price_field[0].send_keys(Keys.TAB)  # Press TAB to move to the next cell
        # price_field[0].send_keys(self.profile.max_rent)
        # price_field[0].send_keys(Keys.RETURN)  # Press RETURN to confirm the input
        
        # # price_field.send_keys(Keys.ENTER)
        # buttons[2].click()
        
        time.sleep(TIME_DELAY_ON_LOAD)
        self.state = "SEARCHED"
    
    def gather_results(self):
        links = self.driver.find_elements(By.XPATH, '//a[@href]')
        valid_links = set()
        for link in links:
            url = link.get_attribute('href')
            if "en/flat/" in url:
                valid_links.add(url)

        return list(valid_links)
    
    def visit_and_gather(self, url: str):
        self.driver.get(url)
        
        match = re.search(r'en/flat/(.*?)/\d+/', url)
        advertisement_id = match.group(1)
        
        time.sleep(1)
        
        content = self.driver.find_element(By.CLASS_NAME, "markdown")
        content_html = content.get_attribute('innerHTML')
        table = self.driver.find_element(By.CSS_SELECTOR, 'table.table--rows.table--fluid.table--fixed.table--flush')
        table_html = table.get_attribute('innerHTML')
        return advertisement_id, content_html + table_html
        
    def send_information(self, message):
        subscription_button = self.driver.find_element(By.ID, "id_create_subscription")
        subscription_button.click()
        text_field = self.driver.find_element(By.ID, "id_text")
        text_field.clear()
        time.sleep(1)
        text_field.send_keys(message)
        time.sleep(1)
        send_button = self.driver.find_element(By.NAME,"contact-advertiser")
        send_button.click()
        # self.driver.execute_script("arguments[0].click();", send_button)
        # @BUG DOES NOT SEND THE MESSAGE
        time.sleep(1000)

    def close(self):
        self.driver.quit()
    
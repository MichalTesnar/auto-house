from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import re

from src.lib.email_client import EmailClient

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
        time.sleep(5)
        code = self.email_client.retrieve_6digit_code()
        otp_field = self.driver.find_element(By.ID, "f1")
        otp_field.send_keys(code)
        consent_button.click()
        self.state = "ENTERED"
    
    def search(self):
        # place_field = self.driver.find_element(By.CLASS_NAME, "mapboxgl-ctrl-geocoder--icon mapboxgl-ctrl-geocoder--icon-search") 
        # place_field.send_keys(self.profile.place)
        # place_field = self.driver.find_element(By.NAME, "Ort")
        # place_field.send_keys(self.profile.place)
        # place_field.send_keys(Keys.RETURN)
        time.sleep(1000)
        self.state = "SEARCHED"
        
    def gather_results(self):
        # Get all links
        links = self.driver.find_elements(By.XPATH, '//a[@href]')
        # Filter
        valid_links = []
        for link in links:
            url = link.get_attribute('href')
            if "https://wohnen.ethz.ch/index.php?act=detoffer&" in url:
                valid_links.append(url)
                
        self.state = "GOT LINKS"
        return valid_links
    
    def visit_and_gather(self, url: str):
        match = re.search(r'pid=(\d+)', url)
        pid = match.group(1)
        
        self.driver.get(url)
        
        time.sleep(TIME_DELAY_ON_LOAD)
        
        section = self.driver.find_element(By.ID, 'contentContainer')
        
        html_content = section.get_attribute('innerHTML')
        
        links = self.driver.find_elements(By.XPATH, '//a[@href]')
        # Filter
        valid_emails = set()
        for link in links:
            email = link.get_attribute('href')
            if "mailto" in email:
                email = email[len("mailto:"):]
                valid_emails.add(email)
        
        if len(valid_emails) > 1:
            raise ValueError("More than one email found: {}".format(valid_emails))
        elif len(valid_emails) == 1:
            email = valid_emails.pop()
            
        return pid, email, html_content
        
         # self.commute_endpoint = data["commute_endpoint"]
            # self.commute_limit_minutes = data["commute_limit_minutes"]
        
        # soup = BeautifulSoup(html_content, 'html.parser')

        # Convert the parsed HTML to an XML tree
        # xml_tree = soup.prettify()
        
        # adresse_row = soup.find('td', class_='fieldlabel', text='Adresse').find_parent('tr')
        
        # if adresse_row:
        #     adresse_cell = adresse_row.find('td', class_='datacell')
        #     if adresse_cell:
        #         address = adresse_cell.get_text(strip=True, separator=' ')
        #         print("Address:", address)
        #     else:
        #         print("Address cell not found")
        # else:
            # print("Adresse row not found")
            
        #https://developers.google.com/maps/documentation/distance-matrix/overview

    def close(self):
        self.driver.quit()
    
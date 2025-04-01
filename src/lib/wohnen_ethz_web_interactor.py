from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import re

TIME_DELAY_ON_LOAD = 0.5
SILENT = False # use driver.get_screenshot_as_file("capture.png") to debug

class WohnenETHZWebInteractor():
    
    def __init__(self, profile):
        self.base_url = "https://wohnen.ethz.ch/index.php?act=searchoffer"
        self.profile = profile

        if SILENT:    
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome()
                
        self.state = "STARTING"
    
    def load(self):
        self.driver.get(self.base_url)
        time.sleep(TIME_DELAY_ON_LOAD)
        self.state = "LOADED"
    
    def enter(self):
        # @ TODO: create a check that it has worked based on the HTML
        username_field = self.driver.find_element(By.NAME, "User")
        username_field.send_keys(self.profile.wohnen_ethz_login)
        password_field = self.driver.find_element(By.NAME, "Passwort")
        password_field.send_keys(self.profile.wohnen_ethz_password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(TIME_DELAY_ON_LOAD)
        self.state = "ENTERED"
    
    def search(self):
        rent_field = self.driver.find_element(By.NAME, "Miete") 
        rent_field.send_keys(self.profile.max_rent)
        place_field = self.driver.find_element(By.NAME, "Ort")
        place_field.send_keys(self.profile.place)
        place_field.send_keys(Keys.RETURN)
        time.sleep(TIME_DELAY_ON_LOAD)
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
            if "mailto" in email and len(email[len("mailto:"):]) > 0:
                
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
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from bs4 import BeautifulSoup


TIME_DELAY = 0.5

class WebInteractor():
    
    def __init__(self):
        with open('secret/site_credentials.json') as f:
            data = json.load(f)
            self.login = data["login"]
            self.password = data["password"]
            self.base_url = data["base_url"]
            
        with open('secret/living_preferences.json') as f:
            data = json.load(f)
            self.place = data["place"]
            self.max_rent = data["budget_upper_bound"]
            self.commute_endpoint = data["commute_endpoint"]
            self.commute_limit_minutes = data["commute_limit_minutes"]
            
        self.driver = webdriver.Chrome()
        self.state = "STARTING"
    
    def load(self):
        self.driver.get(self.base_url)
        time.sleep(TIME_DELAY)
        self.state = "LOADED"
    
    def enter(self):
        # @ TODO: create a check that it has worked based on the HTML
        username_field = self.driver.find_element(By.NAME, "User")
        username_field.send_keys(self.login)
        password_field = self.driver.find_element(By.NAME, "Passwort")
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(TIME_DELAY)
        self.state = "ENTERED"
    
    def search(self):
        rent_field = self.driver.find_element(By.NAME, "Miete") 
        rent_field.send_keys(self.max_rent)
        place_field = self.driver.find_element(By.NAME, "Ort")
        place_field.send_keys(self.place)
        place_field.send_keys(Keys.RETURN)
        time.sleep(TIME_DELAY)
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
        self.driver.get(url)
        
        time.sleep(TIME_DELAY)
        
        section = self.driver.find_element(By.ID, 'contentContainer')
        
        html_content = section.get_attribute('innerHTML')

        soup = BeautifulSoup(html_content, 'html.parser')

        # Convert the parsed HTML to an XML tree
        xml_tree = soup.prettify()
        
        adresse_row = soup.find('td', class_='fieldlabel', text='Adresse').find_parent('tr')
        
        # if adresse_row:
        #     adresse_cell = adresse_row.find('td', class_='datacell')
        #     if adresse_cell:
        #         address = adresse_cell.get_text(strip=True, separator=' ')
        #         print("Address:", address)
        #     else:
        #         print("Address cell not found")
        # else:
            # print("Adresse row not found")

        
        # # print(html_content)
        return html_content

                
                
        # time.sleep(100000)
        
    def close(self):
        self.driver.quit()
    
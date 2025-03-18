from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json


RENT = 800
PLACE = "Zurich"

URL = "https://wohnen.ethz.ch/index.php?act=searchoffer"

with open('secret/site_credentials.json') as f:
    d = json.load(f)
    LOGIN = d["login"]
    PASSWORD = d["password"]

# Set up the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()  # Make sure chromedriver is in your PATH or specify the path

try:
    # Open the website
    driver.get(URL)
    time.sleep(1)  # Wait for the page to load

    # Find the username and password fields and enter the credentials
    username_field = driver.find_element(By.NAME, "User")  # Replace "username" with the actual name/id of the field
    password_field = driver.find_element(By.NAME, "Passwort")  # Replace "password" with the actual name/id of the field

    username_field.send_keys(LOGIN)
    password_field.send_keys(PASSWORD)

    # Submit the form (either by clicking the login button or pressing Enter)
    password_field.send_keys(Keys.RETURN)  # Simulates pressing the Enter key

    # Wait for the login process to complete
    time.sleep(1)  # Adjust the sleep time as needed

    # Optional: Check if login was successful (e.g., by looking for a specific element on the logged-in page)
    # @ TODO: create a check that it has worked based on the HTML

    rent_field = driver.find_element(By.NAME, "Miete")  # Replace "username" with the actual name/id of the field
    rent_field.send_keys(RENT)  # Replace "username" with the actual name/id of the field
    place_field = driver.find_element(By.NAME, "Ort")  # Replace "username" with the actual name/id of the field
    place_field.send_keys(PLACE)

    place_field.send_keys(Keys.RETURN)
    
    time.sleep(1)  # Adjust the sleep time as needed
    # links = driver.find_elements_by_xpath('//a[@href]')
    links = driver.find_elements(By.XPATH, '//a[@href]')

    # Extract and print the URLs
    for link in links:
        url = link.get_attribute('href')
        if "https://wohnen.ethz.ch/index.php?act=detoffer&" in url:
            print(url)
            driver.get(url)
            time.sleep(1000)  # Adjust the sleep time as needed
            
            # scrape adresses
            # extract text
            # return this
            # call LLM
            # create an email
            
            exit()
    
    time.sleep(1000)  # Adjust the sleep time as needed
finally:
    # Close the browser
    driver.quit()
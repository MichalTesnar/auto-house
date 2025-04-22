from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import re
import requests


TIME_DELAY_ON_LOAD = 0.5
SILENT = False  # use driver.get_screenshot_as_file("capture.png") to debug


class FlatfoxWebInteractor:
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
        time.sleep(4)  # give email some time to arrive
        code = self.email_client.retrieve_6digit_code()
        otp_field = self.driver.find_element(By.ID, "f1")
        otp_field.send_keys(code)
        consent_button.click()
        self.state = "ENTERED"

    def search(self):
        time.sleep(1)

        region_field = self.driver.find_element(
            By.CLASS_NAME, "mapboxgl-ctrl-geocoder--input"
        )
        region_field.send_keys(self.profile.place)
        ### LOCATION
        time.sleep(1)
        suggestion_button = self.driver.find_element(
            By.CLASS_NAME, "mapboxgl-ctrl-geocoder--suggestion-address"
        )
        suggestion_button.click()
        region_field.send_keys(Keys.RETURN)

        ### ROOMS
        time.sleep(1)
        buttons = self.driver.find_elements(By.CLASS_NAME, "css-1mtdczm")
        buttons[0].click()
        self.driver.find_element(By.CSS_SELECTOR, 'button[value="SHARED"]').click()
        buttons[0].click()  # close the search for type to be able to open the new one

        ### PRICE
        # Grab the current URL the browser is at
        current_url = self.driver.current_url
        new_url = current_url + f"&max_price={self.profile.max_rent}"
        self.driver.get(new_url)

        time.sleep(1)
        time.sleep(TIME_DELAY_ON_LOAD)
        self.state = "SEARCHED"

    def gather_results(self):
        links = self.driver.find_elements(By.XPATH, "//a[@href]")
        valid_links = set()
        for link in links:
            url = link.get_attribute("href")
            if "en/flat/" in url:
                valid_links.add(url)

        return list(valid_links)

    def visit_and_gather(self, url: str):
        self.driver.get(url)

        match = re.search(r"en/flat/(.*?)/\d+/", url)
        advertisement_id = match.group(1)

        time.sleep(1)

        content = self.driver.find_element(By.CLASS_NAME, "markdown")
        content_html = content.get_attribute("innerHTML")
        table = self.driver.find_element(
            By.CSS_SELECTOR, "table.table--rows.table--fluid.table--fixed.table--flush"
        )
        table_html = table.get_attribute("innerHTML")
        return advertisement_id, content_html + table_html

    def send_information(self, message):
        # Create a requests session
        session = requests.Session()

        # Get CSRF token from the form
        csrf_token_element = self.driver.find_element(By.NAME, "csrfmiddlewaretoken")
        csrf_token = csrf_token_element.get_attribute("value")

        # Transfer cookies from Selenium to requests
        selenium_cookies = self.driver.get_cookies()
        for cookie in selenium_cookies:
            session.cookies.set(cookie["name"], cookie["value"])

        # Prepare headers
        headers = {
            "Referer": self.driver.current_url,
            "User-Agent": "Mozilla/5.0",
        }

        self.profile
        form_data = {
            "csrfmiddlewaretoken": csrf_token,
            "name": self.profile.user_name,
            "email": self.profile.flatfox_login,
            "phone_number": self.profile.user_phone_number,
            "text": message,
            "create_subscription": "off",
        }

        # Submit POST request to the current page
        post_url = self.driver.current_url
        session.post(post_url, data=form_data, headers=headers)
        # response = session.post(post_url, data=form_data, headers=headers)
        # print("✅ Submitted!" if response.ok else f"❌ Failed with {response.status_code}")

        time.sleep(10)

    def close(self):
        self.driver.quit()

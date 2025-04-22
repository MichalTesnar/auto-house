import json

class PersonalProfile():    
    def __init__(self, name: str):
        
        self.name = name
        
        with open(f'secret/{name}/my_description.json') as f:
            data = json.load(f)
            self.user_name = data["Name"]
            self.user_phone_number = data["Phone_number"]
            self.user_email = data["Email"]
            self.description = str(data)
            
        with open(f'secret/{name}/living_preferences.json') as f:
            data = json.load(f)
            self.place_wg_zimmer = data["place_wg_zimmer"]
            self.max_rent_wg_zimmer = int((float(int(data["budget_upper_bound"])) + 49) // 50 * 50) # round up by 50s for the selector
            self.place = data["place"]
            self.max_rent = int(data["budget_upper_bound"])
            
        with open(f'secret/{name}/site_credentials.json') as f:
            data = json.load(f)
            self.wohnen_ethz_login = data["wohnen_ethz_login"]
            self.wohnen_ethz_password = data["wohnen_ethz_password"]
            self.flatfox_login = data["flatfox_login"]
            self.flatfox_password = data["flatfox_password"]
            self.gmail_login = data["login"]
            self.gmail_password = data["password"]
            self.gmail_login2 = data["login2"]
            self.gmail_password2 = data["password2"]
            self.api_key = data["Google_API_KEY"]
            
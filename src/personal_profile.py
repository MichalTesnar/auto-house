import json

class PersonalProfile():    
    def __init__(self, name: str):
        
        self.name = name
        
        with open(f'secret/{name}/gmail_credentials.json') as f:
            data = json.load(f)
            self.gmail_login = data["login"]
            self.gmail_password = data["password"]
            
        with open(f'secret/{name}/my_description.json') as f:
            data = json.load(f)
            self.user_name = data["Name"]
            self.user_phone_number = data["Phone_number"]
            self.user_email = data["Email"]
            
        with open(f'secret/{name}/living_preferences.json') as f:
            data = json.load(f)
            self.place_wg_zimmer = data["place_wg_zimmer"]
            self.max_rent_wg_zimmer = int((data["budget_upper_bound"] + 49) // 50 * 50) # round up by 50s for the selector
            self.place = data["place"]
            self.max_rent = data["budget_upper_bound"]
            
        with open(f'secret/{name}/my_description.json') as f:
            data = json.load(f)
            self.description = str(data)
        
        with open(f'secret/{name}/google_api_credentials.json') as f:
            data = json.load(f)
            self.api_key = data["KEY"]
            
        with open(f'secret/{name}/wohnen_ethz_credentials.json') as f:
            data = json.load(f)
            self.login = data["login"]
            self.password = data["password"]
            